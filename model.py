import openai
import configparser

class Model:

    def __init__(self) -> None:
        openai.api_key = self.read_auth()

    def read_auth(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('OpenAI', 'api_key')
    
    def generate_completion(self, model, prompt):
        completion = openai.Completion.create(model=model, max_tokens=1000, prompt=f"{prompt}\ngenerate a readme file including requirements and usage for this code.")
        return completion
    

if __name__ == "__main__":
    print(Model().generate_completion())