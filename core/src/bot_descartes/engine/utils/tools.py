import json

class Tools:
    def __init__(self):
        self.path_engine = "engine/"
        self.path_cogs = self.path_engine+"cogs/"
        self.path_loops = self.path_cogs+"loops/"

    def load_json(self, path):
        data = None
        with open(path, "r") as f:
            data = json.load(f)
        return data
    
    def save_json(self, path, data):
        with open(path, "w") as f:
            f.write(json.dumps(data, indent=4))