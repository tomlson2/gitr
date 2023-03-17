import openai
import configparser

class Model:

    def __init__(self) -> None:
        openai.api_key = self.read_auth()

    def read_auth(self):
        config = configparser.ConfigParser()
        config.read('config.ini')
        return config.get('OpenAI', 'api_key')
    
    def generate_completion(self, model, prompt, temperature=0.5):
        completion = openai.Completion.create(model=model, temperature=temperature, max_tokens=300, prompt=prompt)
        return completion
    
    def generate_edit(self, model, prompt, instruction, temperature=0.9):
        edit = openai.Edit.create(model=model, input=prompt, instruction=instruction, temperature=temperature)
        print(f'edit: {edit}')
        return edit
    

if __name__ == "__main__":
    print(Model().generate_completion())