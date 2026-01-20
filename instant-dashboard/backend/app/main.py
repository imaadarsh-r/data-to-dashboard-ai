"""FastAPI application for The Instant Dashboard"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from app.config import settings
from app.models import DashboardRequest, DashboardResponse, HealthResponse
from app.llm_service import llm_service
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create FastAPI app
app = FastAPI(
    title="The Instant Dashboard API",
    description="Transform JSON data into beautiful dashboards using AI",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[settings.FRONTEND_URL, "http://localhost:5173", "http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
async def startup_event():
    """Validate configuration on startup"""
    try:
        settings.validate()
        logger.info("✅ Configuration validated successfully")
        logger.info(f"✅ Using model: {settings.GROQ_MODEL}")
    except ValueError as e:
        logger.error(f"❌ Configuration error: {str(e)}")
        raise

@app.get("/", tags=["Root"])
async def root():
    """Root endpoint"""
    return {
        "message": "Welcome to The Instant Dashboard API",
        "docs": "/docs",
        "health": "/health"
    }

@app.get("/health", response_model=HealthResponse, tags=["Health"])
async def health_check():
    """Health check endpoint"""
    groq_configured = bool(settings.GROQ_API_KEY)
    
    return HealthResponse(
        status="healthy" if groq_configured else "unhealthy",
        message="API is running" if groq_configured else "Groq API key not configured",
        groq_configured=groq_configured
    )

@app.post("/generate-dashboard", response_model=DashboardResponse, tags=["Dashboard"])
async def generate_dashboard(request: DashboardRequest):
    """
    Generate a dashboard from JSON data and user instructions
    
    Args:
        request: DashboardRequest with json_data, user_prompt, and optional temperature
        
    Returns:
        DashboardResponse with generated HTML or error
    """
    import time
    
    request_start = time.time()
    
    try:
        logger.info("=" * 60)
        logger.info("📊 NEW DASHBOARD GENERATION REQUEST")
        logger.info("=" * 60)
        logger.info(f"📝 User prompt: {request.user_prompt[:100]}...")
        if request.temperature is not None:
            logger.info(f"🌡️  Custom temperature: {request.temperature}")
        logger.info(f"📦 JSON data size: {len(request.json_data)} chars")
        logger.info("-" * 60)
        
        # Generate dashboard using LLM
        result = llm_service.generate_dashboard(
            json_data_str=request.json_data,
            user_instructions=request.user_prompt,
            temperature=request.temperature
        )
        
        request_time = time.time() - request_start
        
        logger.info("=" * 60)
        logger.info("✅ REQUEST COMPLETED SUCCESSFULLY")
        logger.info(f"⏱️  Total Request Time: {request_time*1000:.2f}ms ({request_time:.2f}s)")
        logger.info(f"📊 Tokens Used: ~{result['tokens_used']:,}")
        logger.info("=" * 60)
        logger.info("")  # Empty line for readability
        
        return DashboardResponse(
            success=True,
            html_content=result['html'],
            error=None,
            metadata={
                'model': result['model'],
                'tokens_used': result['tokens_used'],
                'temperature': result.get('temperature'),
                'latency': result.get('latency', {}),
                'total_request_time_ms': round(request_time * 1000, 2)
            }
        )
        
    except ValueError as e:
        # Validation errors (invalid JSON, etc.)
        logger.error("=" * 60)
        logger.error("❌ VALIDATION ERROR")
        logger.error(f"Error: {str(e)}")
        logger.error("=" * 60)
        logger.error("")
        raise HTTPException(status_code=400, detail=str(e))
        
    except Exception as e:
        # Other errors
        logger.error("=" * 60)
        logger.error("❌ GENERATION ERROR")
        logger.error(f"Error: {str(e)}")
        logger.exception("Full traceback:")
        logger.error("=" * 60)
        logger.error("")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating dashboard: {str(e)}"
        )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        "app.main:app",
        host="0.0.0.0",
        port=settings.BACKEND_PORT,
        reload=True
    )
