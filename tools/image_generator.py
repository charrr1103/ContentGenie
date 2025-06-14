import os
import openai
import requests
from typing import Dict, Optional
from io import BytesIO
from datetime import datetime

class DalleImageGenerator:
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv("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", "")
        openai.api_key = self.api_key if self.api_key else "sk-dummy"

    def generate(self, prompt: str) -> Dict:
        """Generate image using DALL·E 3 with safe initialization"""
        if not self.api_key or self.api_key == "sk-dummy":
            return {
                "success": False,
                "error": "API key not configured",
                "suggestion": "Please set OPENAI_API_KEY environment variable"
            }

        try:
            response = openai.images.generate(
                model="dall-e-3",
                prompt=prompt,
                size="1024x1024",
                quality="standard",
                n=1
            )
            
            image_url = response.data[0].url
            revised_prompt = response.data[0].revised_prompt
            
            # Create directory if it doesn't exist
            os.makedirs("generated_images", exist_ok=True)
            
            # Download and save image
            img_data = requests.get(image_url).content
            filename = f"dalle_{datetime.now().strftime('%Y%m%d_%H%M%S')}.png"
            filepath = os.path.join("generated_images", filename)
            
            with open(filepath, "wb") as f:
                f.write(img_data)
            
            return {
                "success": True,
                "url": image_url,
                "local_path": filepath,
                "revised_prompt": revised_prompt
            }
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }