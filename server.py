from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List

app = FastAPI(
    title="Log Classification API",
    description="A hybrid ML-based log classification system using regex, BERT, and LLM",
    version="1.0.0"
)

# Pydantic models
class LogEntry(BaseModel):
    source: str
    log_message: str

class ClassificationResult(BaseModel):
    source: str
    log_message: str
    target_label: str

class BatchClassificationRequest(BaseModel):
    logs: List[LogEntry]

class BatchClassificationResponse(BaseModel):
    results: List[ClassificationResult]
    total: int
    processed: int

# Lazy load classifier
_classifier = None

def get_classifier():
    global _classifier
    if _classifier is None:
        from classify import classify_log
        _classifier = classify_log
    return _classifier


@app.get("/", tags=["Health"])
def root():
    """Root endpoint - API health check"""
    return {
        "status": "running",
        "message": "Log Classification API is operational",
        "endpoints": {
            "classify_single": "POST /classify",
            "classify_batch": "POST /classify-batch",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }


@app.get("/health", tags=["Health"])
def health_check():
    """Health check endpoint"""
    return {"status": "healthy", "service": "Log Classification API"}


@app.post("/classify", response_model=ClassificationResult, tags=["Classification"])
def classify_single_log(log: LogEntry):
    """Classify a single log entry."""
    try:
        classify_log = get_classifier()
        label = classify_log(log.source, log.log_message)
        return ClassificationResult(
            source=log.source,
            log_message=log.log_message,
            target_label=label
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Classification error: {str(e)}")


@app.post("/classify-batch", response_model=BatchClassificationResponse, tags=["Classification"])
def classify_batch_logs(request: BatchClassificationRequest):
    """Classify multiple log entries in a batch."""
    try:
        classify_log = get_classifier()
        results = []
        for log in request.logs:
            label = classify_log(log.source, log.log_message)
            results.append(ClassificationResult(
                source=log.source,
                log_message=log.log_message,
                target_label=label
            ))
        
        return BatchClassificationResponse(
            results=results,
            total=len(request.logs),
            processed=len(results)
        )
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Batch classification error: {str(e)}")


@app.get("/sample", tags=["Info"])
def get_sample():
    """Get sample classification requests"""
    return {
        "single_example": {
            "source": "LegacyCRM",
            "log_message": "Invoice generation process aborted due to invalid tax calculation"
        },
        "batch_example": {
            "logs": [
                {
                    "source": "ModernCRM",
                    "log_message": "IP 192.168.133.114 blocked due to potential attack"
                },
                {
                    "source": "BillingSystem",
                    "log_message": "User User12345 logged in"
                }
            ]
        }
    }


@app.get("/info", tags=["Info"])
def get_info():
    """Get system and API information"""
    return {
        "name": "Log Classification API",
        "version": "1.0.0",
        "description": "Hybrid ML-based log classification system",
        "supported_sources": ["ModernCRM", "LegacyCRM", "BillingSystem", "AnalyticsEngine", "ModernHR"],
        "classification_methods": ["Regex Pattern Matching", "BERT Embeddings", "LLM (Groq API)"]
    }
