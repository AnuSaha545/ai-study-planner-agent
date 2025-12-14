from typing import Any
import os
from dotenv import load_dotenv
from groq import Groq

load_dotenv()


class AIClient:
    """Client for interacting with Groq LLM API.
    
    Uses llama3-8b-8192 model for structured output generation.
    Designed for deterministic planning tasks (temperature=0.3).
    """
    
    def __init__(self) -> None:
        """Initialize Groq client with API key from environment.
        
        Raises:
            RuntimeError: If GROQ_API_KEY not found in .env
        """
        api_key = os.getenv("GROQ_API_KEY")

        if not api_key:
            raise RuntimeError(
                "GROQ_API_KEY not found. Check your backend/.env file."
            )

        self.client = Groq(api_key=api_key)
        self.model = "llama3-8b-8192"  # Reliable for structured output

    def generate_text(self, prompt: str, **kwargs: Any) -> str:
        """Send prompt to Groq and return model response.
        
        Args:
            prompt: The input prompt for the model
            **kwargs: Additional parameters (reserved for future use)
            
        Returns:
            Model response as string (stripped of whitespace)
            
        Raises:
            groq.APIError: If API call fails
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
        """Summarize text using Groq LLM.
        
        Args:
            text: Text content to summarize
            
        Returns:
            Concise summary of the input text
        """
        prompt = f"Summarize the following text in 2-3 sentences:\n{text}"
        return self.generate_text(prompt)