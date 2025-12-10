from typing import Any
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class AIClient:
    def generate_text(self, prompt: str):
        return "Mock response"

    def summarize(self, text: str):
        return text[:200]


    def __init__(self) -> None:
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError("GROQ_API_KEY not found. Check your backend/.env file.")

        self.client = Groq(api_key=api_key)

        # Reliable for structured output
        self.model = "llama3-8b-8192"


    def generate_text(self, prompt: str, **kwargs: Any) -> str:
        """
        Send prompt to Groq and return model response.
        """
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {
                    "role": "system",
                    "content": "You respond with STRICT valid JSON only when asked. No markdown, no commentary."
                },
                {
                    "role": "user",
                    "content": prompt
                },
            ],
            temperature=0.3,
            max_tokens=2048,
        )

        return response.choices[0].message.content.strip()

    def summarize(self, text: str) -> str:
        prompt = f"Summarize the following text clearly:\n{text}"
        return self.generate_text(prompt)
