import sqlite3
import os
from typing import Dict, Any, List, Optional
from datetime import datetime
import json
from contextlib import contextmanager

class Database:
    def __init__(self):
        self.db_path = os.path.join(os.path.dirname(os.path.dirname(__file__)), 'data', 'ubuntu_language.db')
        os.makedirs(os.path.dirname(self.db_path), exist_ok=True)
        self._init_db()
    
    def _init_db(self):
        """Initialize database with tables"""
        with self._get_db_connection() as conn:
            conn.executescript("""
                CREATE TABLE IF NOT EXISTS users (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    email TEXT UNIQUE NOT NULL,
                    password_hash TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS user_stats (
                    user_id INTEGER PRIMARY KEY,
                    stories_read INTEGER DEFAULT 0,
                    lessons_completed INTEGER DEFAULT 0,
                    practice_sessions INTEGER DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                
                CREATE TABLE IF NOT EXISTS learning_progress (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    language TEXT NOT NULL,
                    resource_type TEXT NOT NULL,
                    resource_id TEXT NOT NULL,
                    progress REAL DEFAULT 0,
                    completed BOOLEAN DEFAULT 0,
                    last_accessed TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                
                CREATE TABLE IF NOT EXISTS achievements (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    description TEXT NOT NULL,
                    earned_date TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    progress REAL DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                
                CREATE TABLE IF NOT EXISTS user_settings (
                    user_id INTEGER PRIMARY KEY,
                    preferred_language TEXT,
                    email_notifications BOOLEAN DEFAULT 0,
                    progress_reminders BOOLEAN DEFAULT 0,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                
                CREATE TABLE IF NOT EXISTS user_preferences (
                    user_id INTEGER PRIMARY KEY,
                    preferred_language TEXT,
                    learning_languages TEXT,  -- Stored as JSON array
                    settings TEXT,  -- Stored as JSON object
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                
                CREATE TABLE IF NOT EXISTS conversations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    language TEXT NOT NULL,
                    topic TEXT NOT NULL,
                    last_context TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users(id)
                );
                
                CREATE TABLE IF NOT EXISTS conversation_messages (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    conversation_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    audio_url TEXT,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (conversation_id) REFERENCES conversations(id)
                );
                
                CREATE TABLE IF NOT EXISTS posts (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    forum TEXT NOT NULL,
                    title TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
                
                CREATE TABLE IF NOT EXISTS saved_resources (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    resource_type TEXT NOT NULL,
                    resource_id TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (user_id) REFERENCES users (id)
                );
                
                CREATE TABLE IF NOT EXISTS translations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    source_text TEXT NOT NULL,
                    source_language TEXT NOT NULL,
                    target_text TEXT NOT NULL,
                    target_language TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
                );
                
                CREATE TABLE IF NOT EXISTS language_training (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    language TEXT NOT NULL,
                    training_type TEXT NOT NULL,
                    training_data TEXT NOT NULL,
                    validation_count INTEGER DEFAULT 0,
                    validation_status TEXT DEFAULT 'pending'
                );
                
                CREATE TABLE IF NOT EXISTS training_validations (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    training_id INTEGER NOT NULL,
                    user_id INTEGER,
                    status TEXT NOT NULL,
                    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                    FOREIGN KEY (training_id) REFERENCES language_training(id)
                );
            """)

    @contextmanager
    def _get_db_connection(self):
        """Create a new database connection for thread-safe operations"""
        conn = sqlite3.connect(self.db_path)
        try:
            yield conn
        finally:
            conn.close()

    def create_user(self, email: str, password_hash: str) -> Dict[str, Any]:
        """Create a new user"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    INSERT INTO users (
                        email, password_hash, created_at
                    ) VALUES (?, ?, CURRENT_TIMESTAMP)
                ''', (email, password_hash))
                
                user_id = cursor.lastrowid
                conn.commit()
                return {
                    'success': True,
                    'user_id': user_id,
                    'email': email
                }
        except sqlite3.IntegrityError:
            return {
                'success': False,
                'error': 'Email already exists'
            }

    def get_user(self, email: str) -> Optional[Dict[str, Any]]:
        """Get user by email"""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT id, email, password_hash, created_at
                FROM users WHERE email = ?
            ''', (email,))
            user = cursor.fetchone()
            
            if user:
                return {
                    'id': user[0],
                    'email': user[1],
                    'password_hash': user[2],
                    'created_at': user[3]
                }
            return None

    def update_user(self, user_id: int, **kwargs) -> Dict[str, Any]:
        """Update user information"""
        allowed_fields = {
            'email'
        }
        
        update_fields = []
        values = []
        
        for key, value in kwargs.items():
            if key in allowed_fields:
                update_fields.append(f"{key} = ?")
                values.append(value)
        
        if not update_fields:
            return {'success': False, 'error': 'No valid fields to update'}
        
        values.append(user_id)  # For WHERE clause
        
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(f'''
                    UPDATE users 
                    SET {', '.join(update_fields)}
                    WHERE id = ?
                ''', values)
                
                if cursor.rowcount > 0:
                    return {'success': True}
                return {'success': False, 'error': 'User not found'}
        except sqlite3.IntegrityError:
            return {'success': False, 'error': 'Email already exists'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def save_resource(self, user_id: int, resource_type: str, resource_id: str) -> dict:
        """Save a learning resource for a user."""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO saved_resources (user_id, resource_type, resource_id) VALUES (?, ?, ?)",
                    (user_id, resource_type, resource_id)
                )
                conn.commit()
                return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_saved_resources(self, user_id: int) -> list:
        """Get all saved resources for a user."""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM saved_resources WHERE user_id = ? ORDER BY created_at DESC",
                    (user_id,)
                )
                resources = cursor.fetchall()
                return [dict(resource) for resource in resources]
        except Exception as e:
            print(f"Error getting saved resources: {e}")
            return []

    def update_learning_progress(self, user_id: int, resource_type: str, resource_id: str, progress: float, completed: bool = False) -> dict:
        """Update learning progress for a user."""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO learning_progress (user_id, resource_type, resource_id, progress, completed)
                    VALUES (?, ?, ?, ?, ?)
                    ON CONFLICT (user_id, resource_type, resource_id)
                    DO UPDATE SET progress = ?, completed = ?, last_accessed = CURRENT_TIMESTAMP
                """, (user_id, resource_type, resource_id, progress, completed, progress, completed))
                conn.commit()
                return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_learning_progress(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's learning progress."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT language, resource_type, progress, completed, last_accessed
                FROM learning_progress
                WHERE user_id = ?
                ORDER BY last_accessed DESC
            """, (user_id,))
            results = cursor.fetchall()
            
            return [
                {
                    'language': row[0],
                    'resource_type': row[1],
                    'progress': row[2],
                    'completed': bool(row[3]),
                    'last_accessed': row[4]
                }
                for row in results
            ]

    def save_translation(self, source_text: str, source_language: str, target_text: str, target_language: str):
        """Save a translation to the database"""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                INSERT INTO translations (source_text, source_language, target_text, target_language)
                VALUES (?, ?, ?, ?)
            ''', (source_text, source_language, target_text, target_language))
            conn.commit()

    def get_recent_translations(self, limit: int = 10) -> List[Dict[str, Any]]:
        """Get recent translations"""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT source_text, source_language, target_text, target_language, created_at
                FROM translations
                ORDER BY created_at DESC
                LIMIT ?
            ''', (limit,))
            
            translations = []
            for row in cursor.fetchall():
                translations.append({
                    'source_text': row[0],
                    'source_language': row[1],
                    'target_text': row[2],
                    'target_language': row[3],
                    'created_at': row[4]
                })
            return translations

    def set_user_preferences(self, user_id: int, preferred_language: str = None, 
                           learning_languages: List[str] = None, settings: Dict[str, Any] = None):
        """Set user preferences"""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            current_values = self.get_user_preferences(user_id)
            
            if current_values:
                # Update existing preferences
                updates = []
                params = []
                if preferred_language is not None:
                    updates.append("preferred_language = ?")
                    params.append(preferred_language)
                if learning_languages is not None:
                    updates.append("learning_languages = ?")
                    params.append(json.dumps(learning_languages))
                if settings is not None:
                    updates.append("settings = ?")
                    params.append(json.dumps(settings))
                
                if updates:
                    query = f"UPDATE user_preferences SET {', '.join(updates)} WHERE user_id = ?"
                    params.append(user_id)
                    cursor.execute(query, params)
            else:
                # Insert new preferences
                cursor.execute('''
                    INSERT INTO user_preferences (user_id, preferred_language, learning_languages, settings)
                    VALUES (?, ?, ?, ?)
                ''', (
                    user_id,
                    preferred_language,
                    json.dumps(learning_languages) if learning_languages else None,
                    json.dumps(settings) if settings else None
                ))
            conn.commit()

    def get_user_preferences(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user preferences"""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('''
                SELECT preferred_language, learning_languages, settings
                FROM user_preferences
                WHERE user_id = ?
            ''', (user_id,))
            
            row = cursor.fetchone()
            if row:
                return {
                    'preferred_language': row[0],
                    'learning_languages': json.loads(row[1]) if row[1] else [],
                    'settings': json.loads(row[2]) if row[2] else {}
                }
            return None

    def sign_in(self, email: str, password: str) -> Dict[str, Any]:
        """Sign in a user with email and password"""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT * FROM users WHERE email = ?', (email,))
            user = cursor.fetchone()
            
            if user:
                # Get column names
                columns = [description[0] for description in cursor.description]
                user_dict = dict(zip(columns, user))
                
                # Update last login time
                cursor.execute(
                    'UPDATE users SET last_login = CURRENT_TIMESTAMP WHERE id = ?',
                    (user_dict['id'],)
                )
                
                # Parse metadata if it exists
                try:
                    metadata = json.loads(user_dict.get('metadata', '{}'))
                except:
                    metadata = {}
                
                return {
                    'success': True,
                    'user': {
                        'id': user_dict['id'],
                        'email': user_dict['email'],
                        'password_hash': user_dict['password_hash'],
                        'metadata': metadata
                    }
                }
            return {'success': False, 'error': 'User not found'}

    def sign_up(self, email: str, password: str, metadata: dict = None) -> Dict[str, Any]:
        """Create a new user account"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    'INSERT INTO users (email, password_hash, metadata) VALUES (?, ?, ?)',
                    (email, password, json.dumps(metadata) if metadata else None)
                )
                return {
                    'success': True,
                    'user_id': cursor.lastrowid,
                    'email': email,
                    'metadata': metadata
                }
        except sqlite3.IntegrityError:
            return {'success': False, 'error': 'Email already exists'}
        except Exception as e:
            return {'success': False, 'error': str(e)}

    def create_post(self, user_id: int, forum: str, title: str, content: str) -> dict:
        """Create a new forum post."""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "INSERT INTO posts (user_id, forum, title, content) VALUES (?, ?, ?, ?)",
                    (user_id, forum, title, content)
                )
                conn.commit()
                return {"success": True, "post_id": cursor.lastrowid}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def get_forum_posts(self, forum: str) -> list:
        """Get all posts for a specific forum."""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM posts WHERE forum = ? ORDER BY created_at DESC",
                    (forum,)
                )
                posts = cursor.fetchall()
                return [dict(post) for post in posts]
        except Exception as e:
            print(f"Error getting forum posts: {e}")
            return []

    def get_user_post_count(self, user_id: int) -> int:
        """Get the number of posts by a user."""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT COUNT(*) FROM posts WHERE user_id = ?",
                    (user_id,)
                )
                return cursor.fetchone()[0]
        except Exception as e:
            print(f"Error getting user post count: {e}")
            return 0

    def get_user_by_id(self, user_id: int) -> dict:
        """Get user by ID."""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute(
                    "SELECT * FROM users WHERE id = ?",
                    (user_id,)
                )
                user = cursor.fetchone()
                return dict(user) if user else None
        except Exception as e:
            print(f"Error getting user by ID: {e}")
            return None

    def save_conversation_state(self, user_id, language, topic, context, messages):
        """Save or update conversation state"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                # Check if conversation exists
                cursor.execute("""
                    SELECT id FROM conversations 
                    WHERE user_id = ? AND language = ? AND topic = ?
                    ORDER BY updated_at DESC LIMIT 1
                """, (user_id, language, topic))
                
                result = cursor.fetchone()
                
                if result:
                    conversation_id = result[0]
                    # Update existing conversation
                    cursor.execute("""
                        UPDATE conversations 
                        SET last_context = ?, updated_at = CURRENT_TIMESTAMP
                        WHERE id = ?
                    """, (context, conversation_id))
                else:
                    # Create new conversation
                    cursor.execute("""
                        INSERT INTO conversations (user_id, language, topic, last_context)
                        VALUES (?, ?, ?, ?)
                    """, (user_id, language, topic, context))
                    conversation_id = cursor.lastrowid

                # Save new messages
                for message in messages:
                    cursor.execute("""
                        INSERT INTO conversation_messages 
                        (conversation_id, role, content, audio_url)
                        VALUES (?, ?, ?, ?)
                    """, (conversation_id, message["role"], message["content"], message.get("audio")))

                conn.commit()
                return True
        except Exception as e:
            print(f"Error saving conversation: {str(e)}")
            return False

    def load_conversation(self, user_id, language, topic):
        """Load the most recent conversation for a user"""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                # Get the most recent conversation
                cursor.execute("""
                    SELECT id, last_context 
                    FROM conversations 
                    WHERE user_id = ? AND language = ? AND topic = ?
                    ORDER BY updated_at DESC LIMIT 1
                """, (user_id, language, topic))
                
                conversation = cursor.fetchone()
                
                if conversation:
                    conversation_id, context = conversation
                    
                    # Get all messages for this conversation
                    cursor.execute("""
                        SELECT role, content, audio_url 
                        FROM conversation_messages 
                        WHERE conversation_id = ?
                        ORDER BY created_at ASC
                    """, (conversation_id,))
                    
                    messages = []
                    for role, content, audio_url in cursor.fetchall():
                        message = {"role": role, "content": content}
                        if audio_url:
                            message["audio"] = audio_url
                        messages.append(message)
                    
                    return {
                        "context": context,
                        "messages": messages
                    }
                return None
        except Exception as e:
            print(f"Error loading conversation: {str(e)}")
            return None

    def get_user_stats(self, user_id: int) -> Optional[Dict[str, Any]]:
        """Get user's learning statistics."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT stories_read, lessons_completed, practice_sessions
                FROM user_stats
                WHERE user_id = ?
            """, (user_id,))
            result = cursor.fetchone()
            
            if result:
                return {
                    'stories_read': result[0],
                    'lessons_completed': result[1],
                    'practice_sessions': result[2]
                }
            return None

    def get_achievements(self, user_id: int) -> List[Dict[str, Any]]:
        """Get user's achievements."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT title, description, earned_date, progress
                FROM achievements
                WHERE user_id = ?
                ORDER BY earned_date DESC
            """, (user_id,))
            results = cursor.fetchall()
            
            return [
                {
                    'title': row[0],
                    'description': row[1],
                    'earned_date': row[2],
                    'progress': row[3]
                }
                for row in results
            ]

    def get_user_settings(self, user_id: int) -> Dict[str, Any]:
        """Get user settings."""
        with self._get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute("""
                SELECT preferred_language, email_notifications, progress_reminders
                FROM user_settings
                WHERE user_id = ?
            """, (user_id,))
            result = cursor.fetchone()
            
            # Return default settings if none exist
            if not result:
                return {
                    'preferred_language': 'Zulu',
                    'email_notifications': False,
                    'progress_reminders': False
                }
            
            return {
                'preferred_language': result[0] or 'Zulu',
                'email_notifications': bool(result[1]),
                'progress_reminders': bool(result[2])
            }

    def update_user_settings(self, user_id: int, settings: Dict[str, Any]) -> bool:
        """Update user settings."""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                cursor.execute("""
                    INSERT INTO user_settings (
                        user_id, preferred_language, email_notifications, progress_reminders
                    ) VALUES (?, ?, ?, ?)
                    ON CONFLICT(user_id) DO UPDATE SET
                        preferred_language = excluded.preferred_language,
                        email_notifications = excluded.email_notifications,
                        progress_reminders = excluded.progress_reminders
                """, (
                    user_id,
                    settings.get('preferred_language', 'Zulu'),
                    settings.get('email_notifications', False),
                    settings.get('progress_reminders', False)
                ))
                conn.commit()
                return True
        except Exception as e:
            print(f"Error updating user settings: {str(e)}")
            return False

    def update_training_validation(self, training_id: int, status: str, user_id: int = None) -> dict:
        """Update the validation status of a training entry."""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Insert validation record
                cursor.execute("""
                    INSERT INTO training_validations (training_id, user_id, status)
                    VALUES (?, ?, ?)
                """, (training_id, user_id, status))
                
                # Update validation count and status in training entry
                cursor.execute("""
                    UPDATE language_training 
                    SET validation_count = validation_count + 1,
                        validation_status = CASE 
                            WHEN validation_count >= 3 THEN 
                                CASE 
                                    WHEN (
                                        SELECT COUNT(*) 
                                        FROM training_validations 
                                        WHERE training_id = ? AND status = 'correct'
                                    ) >= 2 THEN 'verified'
                                    ELSE 'rejected'
                                END
                            ELSE validation_status
                        END
                    WHERE id = ?
                """, (training_id, training_id))
                
                conn.commit()
                return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def update_user_stats(self, user_id: int, stat_type: str) -> dict:
        """Update user statistics."""
        try:
            with self._get_db_connection() as conn:
                cursor = conn.cursor()
                
                # Get current stats
                cursor.execute("""
                    SELECT * FROM user_stats WHERE user_id = ?
                """, (user_id,))
                stats = cursor.fetchone()
                
                if not stats:
                    # Create new stats record if it doesn't exist
                    cursor.execute("""
                        INSERT INTO user_stats (user_id, contributions)
                        VALUES (?, 1)
                    """, (user_id,))
                else:
                    # Update existing stats
                    cursor.execute("""
                        UPDATE user_stats 
                        SET contributions = contributions + 1
                        WHERE user_id = ?
                    """, (user_id,))
                
                conn.commit()
                return {"success": True}
        except Exception as e:
            return {"success": False, "error": str(e)}

# Create a database instance
db = Database()
