import random
from utils.supabase_client import SupabaseClient
from utils.translation import TranslationService

class CulturalGames:
    def __init__(self):
        self.db = SupabaseClient()
        self.translator = TranslationService()

    def get_available_games(self):
        return [
            {
                'id': 'proverb_match',
                'title': 'Match the Proverbs',
                'description': 'Match traditional proverbs with their meanings',
                'difficulty': 'Medium'
            },
            {
                'id': 'cultural_quiz',
                'title': 'Cultural Knowledge Quiz',
                'description': 'Test your knowledge of South African cultures',
                'difficulty': 'Various'
            },
            {
                'id': 'story_completion',
                'title': 'Complete the Story',
                'description': 'Complete traditional stories in different languages',
                'difficulty': 'Hard'
            }
        ]

    def start_game(self, game_id, difficulty='medium'):
        try:
            if game_id == 'proverb_match':
                return self._create_proverb_game(difficulty)
            elif game_id == 'cultural_quiz':
                return self._create_cultural_quiz(difficulty)
            elif game_id == 'story_completion':
                return self._create_story_game(difficulty)
            else:
                return {'error': 'Invalid game ID'}
        except Exception as e:
            print(f"Error starting game: {e}")
            return {'error': str(e)}

    def submit_answer(self, game_id, question_id, answer, user_id):
        try:
            # Verify answer and calculate score
            result = self._verify_game_answer(game_id, question_id, answer)
            
            # Update user progress
            if result['correct']:
                self._update_game_progress(user_id, game_id, result['score'])
            
            return result
        except Exception as e:
            print(f"Error submitting answer: {e}")
            return {'error': str(e)}

    def get_user_achievements(self, user_id):
        try:
            # Get user's game history and calculate achievements
            game_progress = self.db.get_user_progress(user_id)
            achievements = self._calculate_achievements(game_progress)
            return achievements
        except Exception as e:
            print(f"Error getting achievements: {e}")
            return []

    def _create_proverb_game(self, difficulty):
        # Sample proverbs for the game
        proverbs = [
            {
                'proverb': 'Umuntu ngumuntu ngabantu',
                'language': 'Zulu',
                'meaning': 'A person is a person through other people',
                'context': 'Emphasizes the importance of community and interconnectedness'
            },
            # Add more proverbs here
        ]
        
        # Select proverbs based on difficulty
        selected_proverbs = random.sample(proverbs, 5)
        
        return {
            'game_type': 'proverb_match',
            'questions': selected_proverbs,
            'instructions': 'Match each proverb with its correct meaning'
        }

    def _create_cultural_quiz(self, difficulty):
        # Sample quiz questions
        questions = [
            {
                'id': 'q1',
                'question': 'What is the significance of Ubuntu in South African culture?',
                'options': [
                    'A philosophy of human interconnectedness',
                    'A traditional dance',
                    'A type of food',
                    'A religious ceremony'
                ],
                'correct': 0,
                'explanation': 'Ubuntu is a philosophy that emphasizes our interconnectedness'
            },
            # Add more questions here
        ]
        
        return {
            'game_type': 'cultural_quiz',
            'questions': random.sample(questions, 5),
            'instructions': 'Choose the correct answer for each question'
        }

    def _create_story_game(self, difficulty):
        # Sample stories with missing parts
        stories = [
            {
                'title': 'The Story of the First Rainbow',
                'language': 'Xhosa',
                'content': 'Long ago, in a village near the mountains...',
                'missing_parts': [
                    {'position': 3, 'options': ['...', '...', '...']},
                    {'position': 7, 'options': ['...', '...', '...']}
                ]
            },
            # Add more stories here
        ]
        
        return {
            'game_type': 'story_completion',
            'story': random.choice(stories),
            'instructions': 'Complete the story by choosing the correct missing parts'
        }

    def _verify_game_answer(self, game_id, question_id, answer):
        # Implementation would verify answers based on game type
        return {
            'correct': True,  # or False based on verification
            'score': 10,
            'feedback': 'Great job! You understood the cultural context perfectly!'
        }

    def _update_game_progress(self, user_id, game_id, score):
        progress_data = {
            'game_id': game_id,
            'score': score,
            'timestamp': 'NOW()'
        }
        self.db.update_user_progress(user_id, f'game_{game_id}', progress_data)

    def _calculate_achievements(self, game_progress):
        achievements = []
        
        # Example achievement criteria
        total_games = len(game_progress)
        total_score = sum(game['progress'].get('score', 0) for game in game_progress)
        
        if total_games >= 10:
            achievements.append({
                'id': 'cultural_explorer',
                'title': 'Cultural Explorer',
                'description': 'Completed 10 cultural games'
            })
            
        if total_score >= 1000:
            achievements.append({
                'id': 'cultural_master',
                'title': 'Cultural Master',
                'description': 'Earned 1000 points in cultural games'
            })
            
        return achievements
