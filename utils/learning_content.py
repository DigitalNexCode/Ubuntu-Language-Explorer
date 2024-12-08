"""
Learning content management for Ubuntu Language Learning Platform.
Contains structured language learning content and response generation logic.
"""
import random

class LearningContent:
    def __init__(self):
        self.conversation_context = {}
        self.language_data = {
            "zulu": {
                "basics": {
                    "greetings": [
                        ("Sawubona", "Hello"),
                        ("Unjani?", "How are you?"),
                        ("Ngiyaphila", "I am fine"),
                        ("Sala kahle", "Stay well/Goodbye"),
                        ("Hamba kahle", "Go well/Goodbye")
                    ],
                    "responses": [
                        "Yebo", "Cha", "Ngiyabonga", "Kulungile"
                    ]
                },
                "vocabulary": {
                    "numbers": ["kunye", "kubili", "kuthathu", "kune", "kuhlanu"],
                    "family": ["umama", "ubaba", "udadewethu", "umfowethu", "ugogo"],
                    "colors": ["mnyama", "mhlophe", "bomvu", "luhlaza", "phuzi"]
                },
                "grammar": {
                    "noun_classes": ["um-/aba-", "um-/imi-", "i-/ama-", "isi-/izi-"],
                    "tenses": ["present", "past", "future"],
                    "pronouns": ["mina", "wena", "yena", "thina", "nina", "bona"]
                }
            },
            "tswana": {
                "basics": {
                    "greetings": [
                        ("Dumela", "Hello"),
                        ("O kae?", "How are you?"),
                        ("Ke teng", "I am fine"),
                        ("Sala sentle", "Stay well/Goodbye"),
                        ("Tsamaya sentle", "Go well/Goodbye")
                    ],
                    "responses": [
                        "Ee", "Nnyaa", "Ke a leboga", "Go siame"
                    ]
                },
                "vocabulary": {
                    "numbers": ["nngwe", "pedi", "tharo", "nne", "tlhano"],
                    "family": ["mme", "rre", "kgaitsadi", "mogolo", "nkoko"],
                    "colors": ["ntsho", "tshweu", "khibidu", "tala", "serolwana"]
                },
                "grammar": {
                    "noun_classes": ["mo-/ba-", "mo-/me-", "le-/ma-", "se-/di-"],
                    "tenses": ["present", "past", "future"],
                    "pronouns": ["nna", "wena", "ene", "rona", "lona", "bone"]
                }
            }
        }
        
    def initialize_conversation(self, language):
        """Initialize conversation context for a language"""
        self.conversation_context[language] = {
            "state": "greeting",
            "previous_responses": [],
            "practice_mode": False,
            "current_topic": None
        }
        
    def get_conversation_context(self, language):
        """Get the conversation context for a language"""
        return self.conversation_context.get(language)
        
    def set_conversation_context(self, language, context):
        """Set the conversation context for a language"""
        self.conversation_context[language] = context
        
    def get_conversation_response(self, language, message, topic=None):
        """Generate a response based on the conversation context and user message"""
        # Initialize context if not exists
        if language not in self.conversation_context:
            self.initialize_conversation(language)
            
        context = self.conversation_context[language]
        response_data = {
            "text": "",
            "audio_text": "",
            "type": "conversation"
        }
        
        if message.lower() == "start_conversation":
            context["state"] = "greeting"
            context["practice_mode"] = True
            greeting = self.language_data[language]["basics"]["greetings"][0]
            response_data["text"] = f"{greeting[0]}! ({greeting[1]})"
            response_data["audio_text"] = greeting[0]
            return response_data
            
        # Handle greetings
        if context["state"] == "greeting":
            if any(greeting[0].lower() in message.lower() or greeting[1].lower() in message.lower() 
                  for greeting in self.language_data[language]["basics"]["greetings"]):
                response = self.language_data[language]["basics"]["greetings"][1]
                response_data["text"] = f"{response[0]} ({response[1]})"
                response_data["audio_text"] = response[0]
                context["state"] = "conversation"
            else:
                # Help with greeting
                first_greeting = self.language_data[language]["basics"]["greetings"][0]
                response_data["text"] = f"Try greeting me with '{first_greeting[0]}' ({first_greeting[1]})"
                response_data["audio_text"] = first_greeting[0]
            return response_data
            
        # Handle conversation
        if context["state"] == "conversation":
            if any(greeting[1].lower() in message.lower() for greeting in self.language_data[language]["basics"]["greetings"] if "how are you" in greeting[1].lower()):
                response = self.language_data[language]["basics"]["greetings"][2]
                response_data["text"] = f"{response[0]} ({response[1]})"
                response_data["audio_text"] = response[0]
            elif any(greeting[0].lower() in message.lower() for greeting in self.language_data[language]["basics"]["greetings"] if "fine" in greeting[1].lower()):
                response = "Would you like to practice something specific?"
                response_data["text"] = f"{self.language_data[language]['basics']['responses'][3]}! ({response})"
                response_data["audio_text"] = self.language_data[language]['basics']['responses'][3]
                context["state"] = "topic_selection"
            else:
                # Generate response based on topic
                if topic and topic in self.language_data[language]:
                    category = list(self.language_data[language][topic].keys())[0]
                    examples = self.language_data[language][topic][category]
                    if isinstance(examples[0], tuple):
                        example = examples[0]
                        response_data["text"] = f"Let's practice this: {example[0]} ({example[1]})"
                        response_data["audio_text"] = example[0]
                    else:
                        example = examples[0]
                        response_data["text"] = f"Here's a word to practice: {example}"
                        response_data["audio_text"] = example
                else:
                    response_data["text"] = "Would you like to practice greetings, numbers, or family words?"
                    
            return response_data
            
        # Handle topic selection
        if context["state"] == "topic_selection":
            topics = {
                "greetings": self.language_data[language]["basics"]["greetings"],
                "numbers": self.language_data[language]["vocabulary"]["numbers"],
                "family": self.language_data[language]["vocabulary"]["family"]
            }
            
            for topic_name, topic_content in topics.items():
                if topic_name in message.lower():
                    if isinstance(topic_content[0], tuple):
                        example = topic_content[0]
                        response_data["text"] = f"Let's practice {topic_name}. Repeat after me: {example[0]} ({example[1]})"
                        response_data["audio_text"] = example[0]
                    else:
                        response_data["text"] = f"Let's practice {topic_name}. Repeat after me: {topic_content[0]}"
                        response_data["audio_text"] = topic_content[0]
                    context["state"] = "practice"
                    context["current_topic"] = topic_name
                    return response_data
                    
            response_data["text"] = "You can practice greetings, numbers, or family words. Which would you like to try?"
            return response_data
            
        return response_data
        
    def end_practice_mode(self, language):
        """End the practice mode and reset conversation context"""
        if language in self.conversation_context:
            self.conversation_context[language] = {
                "state": "greeting",
                "previous_responses": [],
                "practice_mode": False,
                "current_topic": None
            }
