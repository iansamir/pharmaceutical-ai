import os
import requests
from openai import OpenAI

class Assistant:
    def __init__(
        self,
        system_prompt="You are a personal assistant named Ariana that plans the day, manages appointments, and helps with diet and productivity goals. Respond very briefly, under 30 words.",
        model="gpt-4o-mini", 
        openai_api_key="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"
    ) -> None:
        
        self.client = OpenAI(api_key=openai_api_key)
        self.model = model 
        self.conversation = []
        self.system_prompt = system_prompt
        self.conversation.append({"role": "system", "content": self.system_prompt})
    
    def get_completion(self, prompt, audio=True):
        self.conversation.append({"role": "user", "content": prompt})
        response = self.client.chat.completions.create(
                model=self.model,
                max_tokens=256,
                messages=self.conversation
        )

        completion = response.choices[0].message.content
        self.conversation.append({"role": "assistant", "content": completion})

        return completion

if __name__ == '__main__':
    ariana = Assistant()
    response = ariana.get_completion("hello, who is this")
    print(response) 