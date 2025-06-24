import json
from difflib import get_close_matches
from textblob import TextBlob
from typing import Dict, List, Optional
import random
import speech_recognition as sr
import pyttsx3
import re
import schedule
import time
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import numpy as np
import logging
import os

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

def log_interaction(user_input: str, asena_response: str):
    # Log interactions to a file instead of the console
    with open("interaction_logs.txt", "a") as log_file:
        log_file.write(f"User: {user_input} | Asena: {asena_response}\n")

class Asena:
    def __init__(self):
        self.initialize_components()
        self.knowledge_base = self.load_knowledgebase("src/Knowledge/knowledgebase.json")
        self.conversation_history = self.load_conversation_history("src/Knowledge/history.json")
        self.recognizer, self.engine = self.init_speech()

    def initialize_components(self):
        # Initialize all components of the Asena
        from voice_recognition.recognizer import VoiceRecognizer
        from multitasking.manager import TaskManager
        from smart_learning.learner import SmartLearner
        from humor.jokes import HumorManager
        from problem_solving.solver import ProblemSolver
        from customization.settings import SettingsManager
        from cross_platform.platform_manager import PlatformManager
        from privacy_security.security import SecurityManager
        from api_integrations.integrations import APIIntegrationManager
        from task_automation.automator import TaskAutomator
        
        self.voice_recognizer = VoiceRecognizer()
        self.task_manager = TaskManager()
        self.smart_learner = SmartLearner()
        self.humor_manager = HumorManager()
        self.problem_solver = ProblemSolver()
        self.settings_manager = SettingsManager()
        self.platform_manager = PlatformManager()
        self.security_manager = SecurityManager()
        self.api_integration_manager = APIIntegrationManager()
        self.task_automator = TaskAutomator()

    def init_speech(self):
        recognizer = sr.Recognizer()
        engine = pyttsx3.init()
        voices = engine.getProperty('voices')
        for voice in voices:
            if 'Zira' in voice.name:  # Example of a clear, robotic-sounding voice
                engine.setProperty('voice', voice.id)
                break
        engine.setProperty('rate', 150)  # Adjust speech rate for smoother flow
        return recognizer, engine

    def recognize_speech(self, timeout=None) -> str:
        with sr.Microphone() as source:
            if timeout:
                print(f"You have {timeout} seconds to speak.")
            audio = self.recognizer.listen(source, timeout=timeout)
            try:
                text = self.recognizer.recognize_google(audio)
                print(f"Recognized speech: {text}")  # Debugging information
                return text
            except sr.UnknownValueError:
                print("Speech recognition could not understand audio")  # Debugging information
                return ""
            except sr.RequestError as e:
                print(f"Could not request results from Google Speech Recognition service; {e}")
                return ""

    def recognize_speech_with_retry(self, retries=3):
        for attempt in range(retries):
            try:
                return self.recognize_speech(timeout=5)
            except Exception as e:
                print(f"Attempt {attempt + 1} failed: {e}")
        return "Sorry, I couldn't understand you."

    def speak(self, text: str):
        self.engine.say(text)
        self.engine.runAndWait()

    def clean_text(self, text: str) -> str:
        # Remove characters '#' and '*', and any potential emojis
        text = text.replace("#", "").replace("*", "")
        text = re.sub(r'[^\x00-\x7F]+', '', text)  # Remove emojis and non-ASCII characters
        return text

    def load_knowledgebase(self, file_path: str) -> Dict:
        try:
            with open(file_path, 'r') as file:
                data: Dict = json.load(file)
            if "users" not in data or not isinstance(data["users"], dict):
                print(f"Warning: 'users' key is missing or invalid in '{file_path}'. Initializing with default structure.")
                data["users"] = {"default": {"questions": []}}
            return data
        except FileNotFoundError:
            print(f"Warning: The file '{file_path}' does not exist. Starting with an empty knowledge base.")
            return {"users": {"default": {"questions": []}}}
        except json.JSONDecodeError:
            print(f"Error: The file '{file_path}' contains invalid JSON.")
            return {"users": {"default": {"questions": []}}}

    def save_knowledgebase(self, file_path: str, data: Dict):
        directory = os.path.dirname(file_path)
        if not os.path.exists(directory):
            os.makedirs(directory)
        with open(file_path, 'w') as file:
            json.dump(data, file, indent=2)

    def load_conversation_history(self, file_path: str) -> List[Dict[str, str]]:
        try:
            with open(file_path, 'r') as file:
                data: List[Dict[str, str]] = json.load(file)["history"]
            return data
        except (FileNotFoundError, json.JSONDecodeError):
            print(f"Error: The file '{file_path}' does not exist or contains invalid JSON.")
            return []

    def save_conversation_history(self, file_path: str, history: List[Dict[str, str]]):
        with open(file_path, 'w') as file:
            json.dump({"history": history}, file, indent=2)

    def find_best_match(self, user_question: str) -> Optional[str]:
        # Combine all questions from all users into a single list
        all_questions = []
        for user, data in self.knowledge_base.get("users", {}).items():
            all_questions.extend([q["question"] for q in data.get("questions", [])])

        # Ensure the questions list is not empty
        if not all_questions or all(q.strip() == "" for q in all_questions):
            print("Error: Knowledge base is empty or contains invalid questions.")
            return None

        # Add the user question to the list for comparison
        all_questions_with_input = [user_question] + all_questions

        # Convert questions to TF-IDF vectors
        vectorizer = TfidfVectorizer()
        tfidf_matrix = vectorizer.fit_transform(all_questions_with_input)

        # Calculate cosine similarity between user question and all knowledge base questions
        similarity_scores = cosine_similarity(tfidf_matrix[0:1], tfidf_matrix[1:]).flatten()

        # Find the index of the most similar question
        best_match_index = np.argmax(similarity_scores)

        # Return the best match if similarity is above a threshold
        if similarity_scores[best_match_index] > 0.6:  # Adjust threshold as needed
            return all_questions[best_match_index]
        return None

    def choose_best_response(self, user_input: str, responses: List[str]) -> str:
        # Categorize responses
        categorized_responses = {
            "greetings": ["Hello!", "Hi there!", "Hey! How can I help you?"],
            "farewells": ["Goodbye!", "See you later!", "Take care!"],
            "fallbacks": ["I'm not sure about that.", "Can you rephrase?", "Let me think about that..."],
            "neutral": responses  # Default responses from the knowledge base
        }

        # Analyze sentiment
        blob = TextBlob(user_input)
        polarity = blob.sentiment.polarity

        # Select response based on sentiment
        if polarity > 0.5:
            return random.choice(categorized_responses["greetings"])
        elif polarity < -0.5:
            return random.choice(categorized_responses["farewells"])
        else:
            return random.choice(categorized_responses["neutral"] or categorized_responses["fallbacks"])

    def get_answer_for_question(self, question: str, user_input: str) -> Optional[str]:
        # Access the questions under "users" -> "default"
        questions = self.knowledge_base.get("users", {}).get("default", {}).get("questions", [])
        for q in questions:
            if q["question"].lower() == question.lower():
                if isinstance(q["answer"], list):
                    return self.choose_best_response(user_input, q["answer"])
                return q["answer"]
        return None

    def wake_up_response(self, wake_word: str) -> str:
        # Check for the wake-up word and provide a corresponding response
        wake_responses = {
            "wake up": "I am awake Sarah! How can I assist you today?",
            "hey": "Hey Sarah! I'm awake! What can I do for you?",
            "i am home": "Welcome back home, Sarah! How's it going?",
            "Asena are you up": "Yes, Sarah! I am awake. How are you today?"
        }
        
        # Find the matching response
        for phrase, response in wake_responses.items():
            if phrase in wake_word.lower():
                return response
        
        # Default response if no matching phrase is found
        return "Hello Sarah! I'm here and ready to help!"

    def run(self):
        self.choose_interaction_mode()

    def is_wake_word(self, wake_word: str) -> bool:
        wake_phrases = ["wake up", "hey", "i am home", "asena are you up"]
        return any(phrase in wake_word.lower() for phrase in wake_phrases)

    def handle_wake_up(self, wake_word: str):
        greeting = self.wake_up_response(wake_word)
        print(greeting)
        self.speak(greeting)
        self.handle_conversation()

    def handle_conversation(self):
        while True:
            user_input = self.recognize_speech(timeout=10) or input("You: ")
            if user_input.lower() in ["exit", "quit"]:
                self.exit_asena()
                return
            self.process_command(user_input)

    def exit_asena(self):
        print("Exiting Asena. Have a great day!")
        self.speak("Exiting Asena. Have a great day!")

    def process_command(self, command: str):
        command = self.clean_text(command)
        best_match = self.find_best_match(command)
        if best_match:
            self.handle_known_command(command, best_match)
        else:
            self.handle_unknown_command(command)

    def handle_known_command(self, command: str, best_match: str):
        answer = self.get_answer_for_question(best_match, command)
        print(f"Asena: {answer}")
        self.speak(answer)
        self.save_conversation(command, answer)
        log_interaction(command, answer)  # Logs to a file, not the console

    def handle_unknown_command(self, command: str):
        print("Asena: Sorry, I don't know the answer to that. Can you teach me?")
        self.speak("Sorry, I don't know the answer to that. Can you teach me?")
        new_answer = input('Type the answer or "skip" to skip: ')
        if new_answer.lower() != 'skip':
            # Check if the question already exists in the knowledge base
            # some error is occuring becuase asena is not able to retrive the older chtas
            for user, data in self.knowledge_base["users"].items():
                for q in data["questions"]:
                    if q["question"].lower() == command.lower():
                        print("Asena: This question already exists in the knowledge base.")
                        self.speak("This question already exists in the knowledge base.")
                        return

            # Add the new question and answer to the default user's knowledge base till i learn how to autumate that 
            self.knowledge_base["users"]["default"]["questions"].append({"question": command, "answer": new_answer})
            self.save_knowledgebase('src/Knowledge/knowledgebase.json', self.knowledge_base)
            print('Asena: Thank you! I learned a new response.')
            self.speak('Thank you! I learned a new response.')
        else:
            print("Asena: Okay, let me know if there's anything else I can help with.")
            self.speak("Okay, let me know if there's anything else I can help with.")

    def save_conversation(self, user_input: str, bot_response: str):
        self.conversation_history.append({"user": user_input, "bot": bot_response})
        self.save_conversation_history('src/Knowledge/history.json', self.conversation_history)
        log_interaction(user_input, bot_response)

    def run_scheduler(self):
        self.task_automator.run_scheduler()

    def handle_unknown_question(user_input: str):
        fallback_responses = [
            "I'm not sure about that yet, but I'm learning!",
            "Can you rephrase that?",
            "Interesting question! Let me think..."
        ]
        return random.choice(fallback_responses)

    def choose_interaction_mode(self):
        print("Welcome! How would you like to interact?")
        print("1. Voice Mode")
        print("2. Chat Mode")
        
        while True:
            choice = input("Enter 1 for Voice Mode or 2 for Chat Mode: ").strip()
            if choice == "1":
                print("Voice Mode activated. Say something to wake me up.")
                self.run_voice_mode()
                break
            elif choice == "2":
                print("Chat Mode activated. Type your messages below.")
                self.run_chat_mode()
                break
            else:
                print("Invalid choice. Please enter 1 or 2.")

    def run_voice_mode(self):
        self.run()  # Use the existing `run` method to handle voice-based interaction

    def run_chat_mode(self):
        print("Type 'exit' or 'quit' to end the chat.")
        while True:
            user_input = input("You: ").strip()
            if user_input.lower() in ["exit", "quit"]:
                self.exit_asena()
                break
            self.process_command(user_input)

if __name__ == "__main__":
    asena = Asena()
    asena.choose_interaction_mode()



