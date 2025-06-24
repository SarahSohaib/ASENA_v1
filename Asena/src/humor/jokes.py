class HumorManager:
    def __init__(self):
        self.jokes = [
            "Why did the scarecrow win an award? Because he was outstanding in his field!",
            "I told my computer I needed a break, and now it won't stop sending me beach wallpapers.",
            "Why don't scientists trust atoms? Because they make up everything!",
            "I'm reading a book on anti-gravity. It's impossible to put down!",
            "Why did the math book look sad? Because it had too many problems."
        ]

    def get_random_joke(self):
        import random
        return random.choice(self.jokes)

    def add_joke(self, joke):
        self.jokes.append(joke)

    def customize_jokes(self, new_jokes):
        self.jokes = new_jokes

    def witty_reply(self):
        return "I'm here to assist you, but I can also crack a joke or two!"