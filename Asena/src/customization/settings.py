class SettingsManager:
    def __init__(self):
        self.personality_traits = {
            "humor": True,
            "formal": False,
            "friendly": True,
            "sarcastic": False
        }
        self.interface_settings = {
            "theme": "light",
            "font_size": 12,
            "language": "en"
        }

    def update_personality_trait(self, trait, value):
        if trait in self.personality_traits:
            self.personality_traits[trait] = value
        else:
            raise ValueError("Invalid personality trait.")

    def update_interface_setting(self, setting, value):
        if setting in self.interface_settings:
            self.interface_settings[setting] = value
        else:
            raise ValueError("Invalid interface setting.")

    def get_personality_traits(self):
        return self.personality_traits

    def get_interface_settings(self):
        return self.interface_settings