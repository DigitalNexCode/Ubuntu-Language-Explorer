import streamlit as st
from utils.cultural_games import CulturalGames
from utils.languages import LANGUAGES

def display_game():
    st.title("Ubuntu Language Games")
    st.write("Learn South African languages through interactive cultural games!")

    # Initialize game manager
    games = CulturalGames()
    
    # Language selection
    selected_language = st.selectbox(
        "Choose a language to practice:",
        options=list(LANGUAGES.keys()),
        format_func=lambda x: LANGUAGES[x]["native_name"]
    )

    # Get available games for selected language
    available_games = games.get_available_games(selected_language)
    
    # Game selection
    if available_games:
        game_titles = {game["id"]: game["title"] for game in available_games}
        selected_game = st.selectbox(
            "Choose a game:",
            options=list(game_titles.keys()),
            format_func=lambda x: game_titles[x]
        )
        
        # Get game info
        game_info = next((game for game in available_games if game["id"] == selected_game), None)
        if game_info:
            st.write(f"**{game_info['description']}**")
            
            # Get maximum difficulty for the selected game and language
            max_difficulty = games.get_max_difficulty(selected_game, selected_language)
            
            # Difficulty selection
            if max_difficulty > 1:
                difficulty = st.slider(
                    "Select difficulty level:",
                    min_value=1,
                    max_value=max_difficulty,
                    value=1
                )
                st.write(f"Difficulty: {'🌟' * difficulty}")
            else:
                difficulty = 1
                st.info("This game currently has only one difficulty level.")
            
            # Get available stages for selected difficulty
            available_stages = games.get_available_stages(selected_game, selected_language, difficulty)
            if available_stages:
                stage = st.selectbox(
                    "Select stage:",
                    options=available_stages,
                    format_func=lambda x: f"Stage {x}"
                )
                
                # Game content
                if selected_game == "proverb_match":
                    play_proverb_game(games, selected_language, difficulty, stage)
                elif selected_game == "cultural_quiz":
                    play_cultural_quiz(games, selected_language, difficulty, stage)
                elif selected_game == "story_completion":
                    play_story_completion(games, selected_language, difficulty, stage)
                elif selected_game == "word_association":
                    play_word_association(games, selected_language, difficulty, stage)
                elif selected_game == "memory_match":
                    play_memory_match(games, selected_language, difficulty, stage)
                elif selected_game == "sign_language_practice":
                    play_sign_language_game(games, selected_language, difficulty, stage)
            else:
                st.warning(f"No stages available for difficulty level {difficulty}")
    else:
        st.warning(f"No games available for {LANGUAGES[selected_language]['native_name']} yet. Please check back later!")

def play_proverb_game(games, language, difficulty, stage):
    """Proverb matching game implementation"""
    game_data = games.get_proverb_game(language, difficulty, stage)
    if not game_data or "error" in game_data:
        st.warning("No proverbs available for this language yet.")
        return

    st.subheader("🎯 Proverb Matching Game")
    st.write("Match the proverb with its meaning!")

    # Initialize session state variables
    if 'proverb_score' not in st.session_state:
        st.session_state.proverb_score = 0
    if 'current_proverb_index' not in st.session_state:
        st.session_state.current_proverb_index = 0
    if 'answered_current' not in st.session_state:
        st.session_state.answered_current = False
    if 'show_meaning' not in st.session_state:
        st.session_state.show_meaning = False

    proverbs = game_data["content"]
    total_proverbs = len(proverbs)

    # Show progress
    st.progress((st.session_state.current_proverb_index) / total_proverbs)
    st.write(f"Proverb {st.session_state.current_proverb_index + 1} of {total_proverbs}")
    st.write(f"Score: {st.session_state.proverb_score}/{total_proverbs}")

    if st.session_state.current_proverb_index < total_proverbs:
        current_proverb = proverbs[st.session_state.current_proverb_index]
        
        # Display current proverb
        st.write(f"**Proverb:** {current_proverb['proverb']}")
        
        # Get user's answer
        user_answer = st.text_input(
            "What does this proverb mean?",
            key=f"proverb_{st.session_state.current_proverb_index}",
            disabled=st.session_state.show_meaning
        )

        if user_answer and not st.session_state.show_meaning:
            st.session_state.show_meaning = True
            if user_answer.lower() == current_proverb['meaning'].lower():
                st.success("Correct! 🎉")
                st.session_state.proverb_score += 1
            else:
                st.error(f"Not quite. The meaning is: {current_proverb['meaning']}")
            st.write(f"**Context:** {current_proverb['context']}")

        # Show next button after showing meaning
        if st.session_state.show_meaning:
            if st.button("Next Proverb ➡️"):
                st.session_state.current_proverb_index += 1
                st.session_state.show_meaning = False
                st.experimental_rerun()

    else:
        # Game completed
        st.success(f"🎉 Game completed! Final score: {st.session_state.proverb_score}/{total_proverbs}")
        if st.button("Play Again 🔄"):
            st.session_state.current_proverb_index = 0
            st.session_state.proverb_score = 0
            st.session_state.show_meaning = False
            st.experimental_rerun()

def play_cultural_quiz(games, language, difficulty, stage):
    """Cultural quiz game implementation"""
    game_data = games.get_cultural_quiz(language, difficulty, stage)
    if not game_data or "error" in game_data:
        st.warning("No quiz questions available for this language yet.")
        return

    st.subheader("📚 Cultural Quiz")
    st.write("Test your knowledge of culture and traditions!")

    if 'quiz_score' not in st.session_state:
        st.session_state.quiz_score = 0

    for question in game_data["content"]:
        st.write(f"**Question:** {question['question']}")
        user_answer = st.radio(
            "Choose your answer:",
            question['options'],
            key=f"quiz_{question['question']}"
        )
        if st.button("Check Answer", key=f"check_{question['question']}"):
            if user_answer == question['options'][question['correct']]:
                st.success("Correct! 🎉")
                st.session_state.quiz_score += 1
            else:
                st.error(f"Not quite. The correct answer is: {question['options'][question['correct']]}")
                st.write(f"**Explanation:** {question['explanation']}")

def play_story_completion(games, language, difficulty, stage):
    """Story completion game implementation"""
    game_data = games.get_story_completion(language, difficulty, stage)
    if not game_data or "error" in game_data:
        st.warning("No stories available for this language yet.")
        return

    st.subheader("📖 Story Completion")
    st.write("Complete the story by filling in the missing words!")

    if 'story_score' not in st.session_state:
        st.session_state.story_score = 0

    for story in game_data["content"]:
        st.write(f"**{story['title']}**")
        st.write(story['content'])
        
        for i, missing in enumerate(story['missing_parts']):
            user_answer = st.selectbox(
                f"Fill in blank {i+1}:",
                options=missing['options'],
                key=f"story_{story['title']}_{i}"
            )
            
            if user_answer:
                if user_answer == missing['correct']:
                    st.success("Correct! 🎉")
                    st.session_state.story_score += 1
                else:
                    st.error(f"Not quite. The correct word is: {missing['correct']}")
                st.write(f"**Context:** {missing['context']}")

def play_word_association(games, language, difficulty, stage):
    """Word association game implementation"""
    game_data = games.get_word_association(language, difficulty, stage)
    if not game_data or "error" in game_data:
        st.warning("No word associations available for this language yet.")
        return

    st.subheader("🔤 Word Association")
    st.write("Learn words by category and association!")

    if 'word_score' not in st.session_state:
        st.session_state.word_score = 0

    for category in game_data["content"]:
        st.write(f"**Category: {category['category']}**")
        
        for word, meaning in category['words']:
            col1, col2 = st.columns(2)
            with col1:
                st.write(f"**{word}**")
            with col2:
                user_answer = st.text_input(
                    "What does this word mean?",
                    key=f"word_{word}"
                )
                if user_answer:
                    if user_answer.lower() == meaning.lower():
                        st.success("Correct! 🎉")
                        st.session_state.word_score += 1
                    else:
                        st.error(f"Not quite. The meaning is: {meaning}")

def play_memory_match(games, language, difficulty, stage):
    """Memory matching game implementation"""
    game_data = games.get_memory_match(language, difficulty, stage)
    if not game_data or "error" in game_data:
        st.warning("No memory match content available for this language yet.")
        return

    st.subheader("🎴 Memory Match")
    st.write("Match the words with their translations!")

    if 'memory_score' not in st.session_state:
        st.session_state.memory_score = 0
        st.session_state.matched_pairs = set()

    for category_set in game_data["content"]:
        st.write(f"**Category: {category_set['category']}**")
        
        # Create columns for the matching game
        cols = st.columns(2)
        
        with cols[0]:
            st.write("Words in selected language:")
            pairs = category_set['pairs']
            words = [list(pair.keys())[0] for pair in pairs]
            selected_word = st.radio(
                "Select a word:",
                options=words,
                key=f"word_select_{category_set['category']}"
            )

        with cols[1]:
            st.write("Translations:")
            translations = [list(pair.values())[0] for pair in pairs]
            selected_translation = st.radio(
                "Select the translation:",
                options=translations,
                key=f"trans_select_{category_set['category']}"
            )

        # Check if the pair matches
        if st.button("Check Match", key=f"check_{category_set['category']}"):
            pair_key = f"{selected_word}_{selected_translation}"
            
            # Check if this pair is correct
            is_correct = False
            for pair in pairs:
                if selected_word in pair and pair[selected_word] == selected_translation:
                    is_correct = True
                    break
            
            if is_correct and pair_key not in st.session_state.matched_pairs:
                st.success("Correct match! 🎉")
                st.session_state.memory_score += 1
                st.session_state.matched_pairs.add(pair_key)
            elif pair_key in st.session_state.matched_pairs:
                st.info("You've already matched this pair!")
            else:
                st.error("Not a match. Try again!")

        st.write("---")

def play_sign_language_game(games, language, difficulty, stage):
    """Sign language practice game implementation"""
    game_data = games.get_sign_language_practice(language, difficulty, stage)
    if not game_data or "error" in game_data:
        st.warning("No sign language content available yet.")
        return

    st.subheader("🤟 Sign Language Practice")
    st.write("Learn and practice South African Sign Language!")

    if 'sign_score' not in st.session_state:
        st.session_state.sign_score = 0

    for content in game_data["content"]:
        st.write(f"**Category: {content['category']}**")
        
        for sign in content["signs"]:
            st.write(f"### {sign['word'].title()}")
            
            # Display video if available
            if "video_url" in sign:
                st.video(sign["video_url"])
            
            # Display description and tips
            st.write(f"**How to sign:** {sign['description']}")
            st.info(f"**Practice tip:** {sign['practice_tips']}")
            
            # Practice confirmation
            practiced = st.checkbox(f"I've practiced the sign for '{sign['word']}'", 
                                 key=f"sign_{sign['word']}")
            if practiced:
                st.success("Great job! Keep practicing to improve your signing skills! 🎉")
                st.session_state.sign_score += 1

if __name__ == "__main__":
    display_game()
