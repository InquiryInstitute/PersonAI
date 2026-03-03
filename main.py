"""
personAI - Personal AI Assistant
Main application entry point
"""
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from typing import Optional
from finetuning import FineTuningEngine, FineTuningConfig

load_dotenv()

app = FastAPI(
    title="personAI",
    description="Personal AI Assistant for GitHub, Google Drive, and Web",
    version="0.2.0"
)

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize fine-tuning engine
finetuning_config = FineTuningConfig()
finetuning_engine = FineTuningEngine(finetuning_config)


class Query(BaseModel):
    question: str
    sources: list[str] = ["github", "drive", "web"]


class Response(BaseModel):
    answer: str
    sources: list[dict]
    confidence: float


@app.get("/")
async def root():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "service": "personAI",
        "version": "0.2.0",
        "finetuning_enabled": finetuning_config.enabled
    }


@app.get("/health")
async def health():
    """Detailed health check"""
    return {
        "status": "healthy",
        "read_only_mode": os.getenv("READ_ONLY_MODE", "true").lower() == "true",
        "available_sources": ["github", "drive", "web"],
        "finetuning": {
            "enabled": finetuning_config.enabled,
            "auto": finetuning_config.auto_tune,
            "backend": finetuning_config.backend,
            "require_approval": finetuning_config.require_approval
        }
    }


@app.post("/query", response_model=Response)
async def query(q: Query):
    """
    Query your personal data across GitHub, Google Drive, and the web
    
    Args:
        q: Query object containing question and desired sources
        
    Returns:
        Response with answer, sources, and confidence score
    """
    # TODO: Implement actual query logic
    user_input = q.question
    assistant_output = "This is a placeholder response. Query logic to be implemented."
    
    # Add interaction to fine-tuning buffer
    if finetuning_config.enabled:
        finetuning_engine.add_interaction(user_input, assistant_output)
    
    return Response(
        answer=assistant_output,
        sources=[],
        confidence=0.0
    )


@app.post("/finetune/trigger")
async def trigger_finetuning(num_steps: Optional[int] = None):
    """
    Manually trigger a fine-tuning session
    
    Args:
        num_steps: Number of training steps (defaults to config value)
        
    Returns:
        Training statistics
    """
    if not finetuning_config.enabled:
        raise HTTPException(status_code=400, detail="Fine-tuning is disabled")
    
    if finetuning_config.require_approval:
        # In production, this would check user authentication and approval
        pass
    
    result = finetuning_engine.fine_tune_step(num_steps)
    
    if "error" in result:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result


@app.get("/finetune/stats")
async def get_finetuning_stats():
    """Get fine-tuning statistics"""
    if not finetuning_config.enabled:
        return {"enabled": False}
    
    return {
        "enabled": True,
        "stats": finetuning_engine.get_training_stats(),
        "config": {
            "auto": finetuning_config.auto_tune,
            "backend": finetuning_config.backend,
            "learning_rate": finetuning_config.learning_rate,
            "steps_per_session": finetuning_config.steps_per_session
        }
    }


@app.post("/finetune/rollback")
async def rollback_model(checkpoint_name: Optional[str] = None):
    """
    Rollback model to a previous checkpoint
    
    Args:
        checkpoint_name: Name of checkpoint to rollback to (or latest if None)
        
    Returns:
        Success status
    """
    if not finetuning_config.enabled or not finetuning_config.rollback_enabled:
        raise HTTPException(status_code=400, detail="Rollback is disabled")
    
    success = finetuning_engine.rollback(checkpoint_name)
    
    if not success:
        raise HTTPException(status_code=500, detail="Rollback failed")
    
    return {"status": "success", "checkpoint": checkpoint_name or "latest"}


@app.get("/finetune/buffer")
async def get_conversation_buffer():
    """Get current conversation buffer for review"""
    if not finetuning_config.enabled:
        raise HTTPException(status_code=400, detail="Fine-tuning is disabled")
    
    return {
        "messages": finetuning_engine.buffer.messages,
        "training_pairs": finetuning_engine.buffer.get_training_pairs(),
        "buffer_size": len(finetuning_engine.buffer.messages),
        "max_size": finetuning_engine.buffer.max_size
    }


@app.post("/index/github")
async def index_github():
    """Index GitHub repositories for faster querying"""
    # TODO: Implement GitHub indexing
    return {"status": "not_implemented"}


@app.post("/index/drive")
async def index_drive():
    """Index Google Drive for faster querying"""
    # TODO: Implement Drive indexing
    return {"status": "not_implemented"}


if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8080))
    uvicorn.run(app, host="0.0.0.0", port=port)
