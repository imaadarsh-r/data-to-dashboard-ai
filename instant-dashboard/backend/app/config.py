import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

class Settings:
    """Application configuration settings"""
    
    # Groq API Configuration
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "")
    GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile")
    
    # Server Configuration
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    FRONTEND_URL: str = os.getenv("FRONTEND_URL", "http://localhost:5173")
    
    # API Configuration
    MAX_TOKENS: int = 4096
    TEMPERATURE: float = 0.3
    
    def validate(self):
        """Validate that required settings are present"""
        if not self.GROQ_API_KEY:
            raise ValueError(
                "GROQ_API_KEY is required. Please set it in your .env file.\n"
                "Get your API key from: https://console.groq.com/keys"
            )
        return True

# Create settings instance
settings = Settings()
