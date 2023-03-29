import openai
import configparser

class Model:

    def __init__(self) -> None:
        openai.api_key = self.read_auth()

    def read_auth(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('OpenAI', 'api_key')
    
    def generate_completion(self, model, prompt, max_tokens=4000, temperature=0.5):
        print("generating...")
        completion = openai.ChatCompletion.create(model=model, temperature=temperature, max_tokens=max_tokens, messages=[{"role": "user", "content": prompt}])
        print(completion)
        return completion
    
    def generate_edit(self, model, prompt, instruction, temperature=0.9):
        edit = openai.Edit.create(model=model, input=prompt, instruction=instruction, temperature=temperature)
        return edit
    

if __name__ == "__main__":
    print(Model().generate_completion())