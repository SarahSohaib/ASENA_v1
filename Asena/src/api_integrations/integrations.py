class APIIntegrationManager:
    def __init__(self):
        self.integrations = {}

    def add_integration(self, name, api_client):
        self.integrations[name] = api_client

    def remove_integration(self, name):
        if name in self.integrations:
            del self.integrations[name]

    def get_integration(self, name):
        return self.integrations.get(name)

    def fetch_data(self, name, endpoint, params=None):
        if name in self.integrations:
            response = self.integrations[name].get(endpoint, params=params)
            return response.json() if response.ok else None
        return None

    def list_integrations(self):
        return list(self.integrations.keys())