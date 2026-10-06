import requests


class OllamaClient:
    def __init__(
        self,
        model="qwen3:8b",
        base_url="http://localhost:11434",
    ):
        self.model = model
        self.base_url = base_url.rstrip("/")

    def generate(self, prompt):
        url = f"{self.base_url}/api/generate"

        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "think": False,
            "options": {
                "temperature": 0.2,
                "num_predict": 150,
            },
        }

        response = requests.post(
            url,
            json=payload,
            timeout=300,
        )

        response.raise_for_status()

        data = response.json()

        return data.get("response", "").strip()