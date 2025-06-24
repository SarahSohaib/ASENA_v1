from textblob import TextBlob
import json
from difflib import get_close_matches
from typing import Dict, List, Optional
import random

# Drag this dusty knowledge base from wherever it's hiding
def load_knowledgebase(file_path: str) -> Dict:
    try:
        with open(file_path, 'r') as file:
            data: Dict = json.load(file)
        return data
    except (FileNotFoundError, json.JSONDecodeError):
        print(f"Error: The file '{file_path}' does not exist or contains invalid JSON.")
        return {"questions": []}

# Carefully save the precious knowledge base so it doesn't get lost in the void
def save_knowledgebase(file_path: str, data: Dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)

# Try to find the best match, because apparently guessing is not good enough
def find_best_match(user_question: str, questions: List[str]) -> Optional[str]:
    matches = get_close_matches(user_question.lower(), [q.lower() for q in questions], n=1, cutoff=0.6)
    return matches[0] if matches else None


# Pick a response based on whether you're being nice, mean, or just boring
def choose_best_response(user_input: str, responses: List[str]) -> str:
    # Let's analyze your mood like we're mind readers
    blob = TextBlob(user_input)
    polarity = blob.sentiment.polarity  # Because clearly, numbers determine emotions

    if polarity > 0.5:  # Oh, you're in a good mood? Let me ruin it.
        positive_responses = [resp for resp in responses if "great" in resp or "awesome" in resp]
        return random.choice(positive_responses) if positive_responses else random.choice(responses)
    elif polarity < -0.5:  # Someone's having a bad day, huh?
        negative_responses = [resp for resp in responses if "sorry" in resp or "help" in resp]
        return random.choice(negative_responses) if negative_responses else random.choice(responses)
    else:  # Neutral? Boring.
        neutral_responses = [resp for resp in responses if "hello" in resp or "assist" in resp]
        return random.choice(neutral_responses) if neutral_responses else random.choice(responses)

# Attempt to fetch an answer for your question. Fingers crossed!
def get_answer_for_question(question: str, knowledge_base: Dict, user_input: str) -> Optional[str]:
    for q in knowledge_base["questions"]:
        if q["question"] == question:
            # Oh, a list of answers? Fancy. Let's pick one.
            if isinstance(q["answer"], list):
                return choose_best_response(user_input, q["answer"])
            return q["answer"]
    return None  # Shocking, we found nothing.

# The main event: Asena graces you with its sarcastic brilliance
def chat_bot():
    knowledge_base: Dict = load_knowledgebase("knowledgebase.json")

    while True:
        user_input: str = input("You: ")

        if user_input.lower() == 'quit':
            print("Asena: Goodbye! Have a great day, or don't. Your choice.")
            break

        # Time to play "match the question to the database". Thrilling.
        best_match: Optional[str] = find_best_match(user_input, [q["question"] for q in knowledge_base["questions"]])

        if best_match:
            answer: str = get_answer_for_question(best_match, knowledge_base, user_input)
            print(f"Asena: {answer}")
        else:
            print("Asena: Sorry, I don't know the answer to that. Can you teach me? Because clearly, I can't know everything.")
            new_answer: str = input('Type the answer or "skip" to skip: ')

            if new_answer.lower() != 'skip':
                knowledge_base["questions"].append({"question": user_input, "answer": new_answer})
                save_knowledgebase('knowledgebase.json', knowledge_base)
                print('Asena: Thank you! I learned a new response. Guess I’m doing your job now.')

# Start the Asena Show, starring your questions and my patience
if __name__ == "__main__":
    chat_bot()
