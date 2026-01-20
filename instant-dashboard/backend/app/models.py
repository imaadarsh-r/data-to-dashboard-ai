from pydantic import BaseModel, Field, validator
from typing import Any, Optional
import json

class DashboardRequest(BaseModel):
    """Request model for dashboard generation"""
    json_data: str = Field(..., description="JSON data as a string")
    user_prompt: str = Field(..., description="User instructions for dashboard design")
    temperature: Optional[float] = Field(default=None, ge=0.0, le=2.0, description="LLM temperature (0.0-2.0)")
    
    @validator('json_data')
    def validate_json(cls, v):
        """Validate that json_data is valid JSON"""
        try:
            # Try to parse the JSON to ensure it's valid
            parsed = json.loads(v)
            # Return the original string (we'll parse it again in the service)
            return v
        except json.JSONDecodeError as e:
            raise ValueError(f"Invalid JSON: {str(e)}")
    
    @validator('user_prompt')
    def validate_prompt(cls, v):
        """Validate that user_prompt is not empty"""
        if not v or not v.strip():
            raise ValueError("User prompt cannot be empty")
        return v.strip()

class DashboardResponse(BaseModel):
    """Response model for dashboard generation"""
    success: bool
    html_content: Optional[str] = None
    error: Optional[str] = None
    metadata: Optional[dict] = None
    
    class Config:
        json_schema_extra = {
            "example": {
                "success": True,
                "html_content": "<!DOCTYPE html><html>...</html>",
                "error": None,
                "metadata": {
                    "model": "llama-3.3-70b-versatile",
                    "tokens_used": 1234
                }
            }
        }

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    message: str
    groq_configured: bool
