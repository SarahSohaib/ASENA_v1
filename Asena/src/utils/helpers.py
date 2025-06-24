def load_config(file_path):
    import json
    with open(file_path, 'r') as file:
        return json.load(file)

def save_config(file_path, config):
    import json
    with open(file_path, 'w') as file:
        json.dump(config, file, indent=4)

def generate_unique_id():
    import uuid
    return str(uuid.uuid4())

def format_response(response):
    return response.strip().capitalize()

def log_event(event_message):
    import logging
    logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')
    logging.info(event_message)