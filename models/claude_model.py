from models.base_model import BaseModel

class ClaudeModel(BaseModel):
    def generate(self, prompt: str) -> str:
        # TODO: Replace with actual Claude API call
        return f"[Claude simulated response] for: {prompt}"