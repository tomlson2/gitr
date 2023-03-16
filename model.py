import os
import openai

class Model:

    def __init__(self) -> None:
        openai.api_key = self.read_auth()
        self.model = "text-davinci-003"

    def read_auth(self):
        with open('key.txt', 'r') as file:
            auth_key = file.readline().strip()
        return auth_key
    
    def generate_completion(self, prompt):
        completion = openai.Completion.create(model="text-davinci-003", prompt=f"{prompt}\ngenerate a readme file including requirements and usage for this code.")
        return completion


if __name__ == "__main__":
    print(Model().generate_completion())