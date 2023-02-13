import json

class Config:
    def __init__(self):
        with open("config.json", "r") as config_file:
            config_dict = json.load(config_file)

        for key, value in config_dict.items():
            setattr(self, key, value)

