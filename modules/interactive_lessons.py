import json
from utils.supabase_client import SupabaseClient
from utils.translation import TranslationService
from utils.audio import AudioService

class LearningModule:
    def __init__(self):
        self.db = SupabaseClient()
        self.translator = TranslationService()
        self.audio = AudioService()

    def get_lesson(self, module_id, user_id):
        try:
            # Get user's progress
            progress = self.db.get_user_progress(user_id, module_id)
            current_level = progress.get('level', 1) if progress else 1
            
            # Load lesson content based on level
            lesson = self._load_lesson_content(module_id, current_level)
            return lesson
        except Exception as e:
            print(f"Error loading lesson: {e}")
            return None

    def submit_exercise(self, user_id, module_id, exercise_id, answer):
        try:
            # Get exercise details and verify answer
            exercise = self._get_exercise(exercise_id)
            if not exercise:
                return {'success': False, 'message': 'Exercise not found'}

            is_correct = self._verify_answer(exercise, answer)
            
            # Update progress
            progress_data = {
                'last_exercise': exercise_id,
                'is_correct': is_correct,
                'timestamp': 'NOW()'
            }
            
            self.db.update_user_progress(user_id, module_id, progress_data)
            
            return {
                'success': True,
                'is_correct': is_correct,
                'feedback': self._generate_feedback(exercise, is_correct)
            }
        except Exception as e:
            print(f"Error submitting exercise: {e}")
            return {'success': False, 'message': str(e)}

    def get_progress_summary(self, user_id):
        try:
            # Get all progress records for user
            progress_records = self.db.get_user_progress(user_id)
            
            summary = {
                'total_modules': len(progress_records),
                'completed_modules': 0,
                'total_exercises': 0,
                'correct_exercises': 0,
                'achievements': []
            }
            
            for record in progress_records:
                progress = record.get('progress', {})
                summary['total_exercises'] += progress.get('total_exercises', 0)
                summary['correct_exercises'] += progress.get('correct_exercises', 0)
                
                if progress.get('completed', False):
                    summary['completed_modules'] += 1
                    
                # Check and award achievements
                new_achievements = self._check_achievements(progress)
                summary['achievements'].extend(new_achievements)
            
            return summary
        except Exception as e:
            print(f"Error getting progress summary: {e}")
            return None

    def _load_lesson_content(self, module_id, level):
        # This would typically load from a content management system or database
        # For now, we'll return a sample lesson structure
        return {
            'module_id': module_id,
            'level': level,
            'title': f'Level {level} Lesson',
            'content': {
                'introduction': 'Welcome to the lesson',
                'vocabulary': ['word1', 'word2', 'word3'],
                'grammar': 'Grammar explanation',
                'exercises': self._generate_exercises(level)
            }
        }

    def _generate_exercises(self, level):
        # Generate appropriate exercises based on level
        return [
            {
                'id': f'ex_{level}_1',
                'type': 'multiple_choice',
                'question': 'Sample question',
                'options': ['option1', 'option2', 'option3'],
                'correct_answer': 'option1'
            }
        ]

    def _verify_answer(self, exercise, user_answer):
        if exercise['type'] == 'multiple_choice':
            return user_answer == exercise['correct_answer']
        # Add more verification types as needed
        return False

    def _generate_feedback(self, exercise, is_correct):
        if is_correct:
            return "Correct! Well done!"
        return f"Not quite right. The correct answer was: {exercise['correct_answer']}"

    def _check_achievements(self, progress):
        achievements = []
        
        # Example achievement criteria
        if progress.get('correct_exercises', 0) >= 10:
            achievements.append({
                'id': 'achievement_10_correct',
                'title': '10 Correct Answers',
                'description': 'Completed 10 exercises correctly'
            })
            
        return achievements
