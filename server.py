from fastapi import FastAPI, HTTPException, File, UploadFile
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from typing import List
import pandas as pd
from io import StringIO, BytesIO
import os

from classify import classify_log, classify_csv

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


@app.get("/", tags=["Health"])
def root():
    """Root endpoint - API health check"""
    return {
        "status": "running",
        "message": "Log Classification API is operational",
        "endpoints": {
            "classify_single": "POST /classify",
            "classify_batch": "POST /classify-batch",
            "classify_csv": "POST /classify-csv",
            "download_sample": "GET /sample-csv",
            "docs": "/docs",
            "openapi": "/openapi.json"
        }
    }


@app.post("/classify", response_model=ClassificationResult, tags=["Classification"])
def classify_single_log(log: LogEntry):
    """
    Classify a single log entry.
    
    **Parameters:**
    - `source`: The system source of the log (e.g., "ModernCRM", "LegacyCRM", "BillingSystem")
    - `log_message`: The log message to classify
    
    **Returns:**
    - Classification result with predicted label
    
    **Example:**
    ```json
    {
        "source": "LegacyCRM",
        "log_message": "Invoice generation process aborted due to invalid tax calculation"
    }
    ```
    """
    try:
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
    """
    Classify multiple log entries in a batch.
    
    **Parameters:**
    - `logs`: List of log entries with source and log_message
    
    **Returns:**
    - Batch classification results
    
    **Example:**
    ```json
    {
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
    ```
    """
    try:
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


@app.post("/classify-csv", tags=["CSV Processing"])
async def classify_csv_file(file: UploadFile = File(...)):
    """
    Upload a CSV file and get classified results.
    
    **CSV Format:**
    The CSV should have exactly two columns:
    - `source`: Log source system
    - `log_message`: The log message to classify
    
    **Returns:**
    - CSV file with an additional `target_label` column
    
    **Example CSV:**
    ```
    source,log_message
    ModernCRM,"IP 192.168.133.114 blocked due to potential attack"
    BillingSystem,"User User12345 logged in"
    ```
    """
    try:
        if not file.filename.endswith('.csv'):
            raise HTTPException(status_code=400, detail="File must be a CSV file")
        
        contents = await file.read()
        df = pd.read_csv(StringIO(contents.decode('utf-8')))
        
        if not all(col in df.columns for col in ['source', 'log_message']):
            raise HTTPException(
                status_code=400,
                detail="CSV must contain 'source' and 'log_message' columns"
            )
        
        logs = list(zip(df['source'], df['log_message']))
        from classify import classify
        labels = classify(logs)
        df['target_label'] = labels
        
        output = BytesIO()
        df.to_csv(output, index=False)
        output.seek(0)
        
        return FileResponse(
            path=output,
            media_type="text/csv",
            filename="classified_logs.csv"
        )
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"CSV processing error: {str(e)}")


@app.get("/sample-csv", tags=["CSV Processing"])
def download_sample_csv():
    """
    Download a sample CSV file to understand the expected format.
    
    **Format:**
    - Column 1: `source` - The system source of the log
    - Column 2: `log_message` - The log message text
    """
    sample_data = """source,log_message
ModernCRM,"IP 192.168.133.114 blocked due to potential attack"
BillingSystem,"User User12345 logged in"
AnalyticsEngine,"File data_6957.csv uploaded successfully by user user265"
AnalyticsEngine,"Backup completed successfully"
ModernHR,"GET/V2/54FADB412C4E40CDBAED 9335c4c35a9e/servers/detail - HTTP/1/RCODE 200 len: 1583 time: 01878400"
ModernHR,"Admin access escalation detected for user 9429"
LegacyCRM,"Case escalation for ticket ID 7324 failed because the assigned support agent is no longer active."
LegacyCRM,"Invoice generation process aborted for order ID 8910 due to invalid tax calculation module."
LegacyCRM,"The 'Bulk Email/Sender' feature is no longer supported. Use 'EmailCampaignManager' for imposed functions."
LegacyCRM,"The 'ReportGenerator' module will be retired in version 4.0, please migrate to the 'AdvancedAnalytics'"""
    
    output = StringIO(sample_data)
    return FileResponse(
        path=StringIO(sample_data),
        media_type="text/csv",
        filename="sample_logs.csv"
    )


@app.get("/health", tags=["Health"])
def health_check():
    """
    Health check endpoint for monitoring.
    
    **Returns:**
    - Status of the classification service
    """
    return {
        "status": "healthy",
        "service": "Log Classification API",
        "version": "1.0.0"
    }


@app.get("/info", tags=["Info"])
def get_info():
    """
    Get information about the classification system.
    
    **Returns:**
    - Details about available classifiers and supported sources
    """
    return {
        "name": "Log Classification System",
        "version": "1.0.0",
        "description": "Hybrid ML-based log classification using regex, BERT, and LLM",
        "classifiers": {
            "regex": "Fast pattern matching for common log types",
            "bert": "BERT embeddings with pre-trained logistic regression model",
            "llm": "LLaMA 3.3 70B via Groq API (for LegacyCRM logs)"
        },
        "supported_sources": [
            "ModernCRM",
            "BillingSystem",
            "AnalyticsEngine",
            "ModernHR",
            "LegacyCRM"
        ],
        "classification_categories": [
            "User Action",
            "System Notification",
            "Workflow Error",
            "Deprecation Warning",
            "Unclassified"
        ]
    }


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
