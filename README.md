# Classification Logs

A machine learning-based log classification system that categorizes logs from multiple enterprise systems using a hybrid approach combining regex patterns, BERT embeddings, and LLM-based classification.

## Overview

This project classifies system logs into predefined categories using three complementary classification strategies:

1. **Regex-based Classification**: Fast pattern matching for common log types
2. **BERT-based Classification**: Neural network classification using sentence transformers and a pre-trained logistic regression model
3. **LLM-based Classification**: GPT-powered classification for complex logs (specifically for LegacyCRM logs)

## Features

- **Multi-source Support**: Handles logs from different enterprise systems (ModernCRM, BillingSystem, AnalyticsEngine, ModernHR, LegacyCRM)
- **Hybrid Classification Strategy**: Falls back to more sophisticated methods when simpler ones fail
- **CSV Input/Output**: Batch process logs from CSV files
- **Pre-trained Models**: Includes a trained BERT-based classifier model
- **Extensible Architecture**: Easy to add new classification methods or system-specific logic

## Project Structure

```
.
├── classify.py              # Main classification orchestrator
├── processor_regex.py       # Regex-based pattern matching classifier
├── processor_bert.py        # BERT embeddings + ML model classifier
├── processor_llm.py         # LLM-based classifier (Groq API)
├── Training/                # Pre-trained models and training scripts
│   └── model/
│       └── log_classifier.joblib
├── resources/               # Input/output CSV files
│   ├── test.csv            # Sample input logs
│   └── output.csv          # Classification results
├── pyproject.toml          # Project dependencies
└── .env                    # Environment variables (API keys)
```

## Installation

### Prerequisites

- Python 3.13+
- pip or uv package manager

### Setup

1. **Clone/navigate to the project**:
   ```bash
   cd "Classification Logs"
   ```

2. **Create virtual environment**:
   ```bash
   python -m venv .venv
   .venv\Scripts\activate  # Windows
   # or: source .venv/bin/activate  # Linux/Mac
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   # or using uv:
   uv pip install -r requirements.txt
   ```

4. **Set up environment variables**:
   Create a `.env` file with your Groq API key:
   ```
   GROQ_API_KEY=your_key_here
   ```

   Get your key from: https://console.groq.com/keys

## Setup Instructions

### Install Dependencies

Make sure you have Python installed on your system. Install the required Python libraries by running the following command:

```bash
pip install -r requirements.txt
```

### Run the FastAPI Server

To start the server, use the following command:

```bash
uvicorn server:app --reload
```

Once the server is running, you can access the API at:

- **Main endpoint**: http://127.0.0.1:8000/
- **Interactive Swagger documentation**: http://127.0.0.1:8000/docs
- **Alternative API documentation**: http://127.0.0.1:8000/redoc

## Usage

### Basic Usage

Run the classifier on the sample CSV file:
```bash
python classify.py
```

This will:
1. Read `resources/test.csv`
2. Classify each log entry
3. Output results to `resources/output.csv` with a new `target_label` column

### Input CSV Format

The input CSV should have two columns:
```csv
source,log_message
ModernCRM,"Your log message here"
BillingSystem,"Another log message"
```

### Classification Pipeline

For each log, the system:

1. **Checks the source**:
   - If `LegacyCRM`: Use LLM classifier
   - Otherwise: Try regex patterns first

2. **If regex matches**: Return the label
3. **If no regex match**: Use BERT classifier
4. **If BERT confidence < 0.5**: Return "Unclassified"

### Classification Categories

**Regex patterns detect**:
- User Action
- System Notification

**BERT/LLM patterns detect**:
- Workflow Error
- Deprecation Warning
- Unclassified (fallback)

## Classification Methods

### Regex Classifier (`processor_regex.py`)

Fast pattern matching using predefined regex rules:
- User login/logout actions
- Backup events
- System updates
- File uploads
- Disk cleanup
- System reboots

**Pros**: Fast, deterministic, no GPU needed
**Cons**: Limited to predefined patterns

### BERT Classifier (`processor_bert.py`)

Uses sentence embeddings (all-MiniLM-L6-v2) with a trained logistic regression model.

**Model**: 
- Transformer: `sentence-transformers/all-MiniLM-L6-v2`
- Classifier: LogisticRegression (scikit-learn)
- Path: `Training/model/log_classifier.joblib`

**Pros**: Semantic understanding, handles unseen patterns
**Cons**: Requires GPU/compute resources, depends on training data quality

### LLM Classifier (`processor_llm.py`)

Uses Groq's LLaMA 3.3 70B model for complex classification decisions.

**Model**: `llama-3.3-70b-versatile`
**API Provider**: Groq (https://groq.com)

**Pros**: State-of-the-art reasoning, handles complex logic
**Cons**: Requires API key, slower, higher cost

## Dependencies

- **groq** (>=1.5.0): LLM API client
- **pandas** (>=3.0.3): CSV handling and data manipulation
- **sentence-transformers** (>=5.6.0): BERT embeddings
- **scikit-learn**: Machine learning models (via sentence-transformers)
- **python-dotenv** (>=1.2.2): Environment variable management
- **jupyterlab** (>=4.6.0): Interactive notebooks
- **ipykernel** (>=7.3.0): Jupyter kernel support

## Configuration

### Environment Variables

Create a `.env` file:
```
GROQ_API_KEY=gsk_xxxxx...
HF_TOKEN=hf_xxxxx...  # Optional, for Hugging Face model caching
```

## Example

```python
from classify import classify_log

# Classify a single log
label = classify_log("LegacyCRM", "Invoice generation process failed")
print(label)  # Output: Workflow Error

# Classify multiple logs
from classify import classify

logs = [
    ("ModernCRM", "IP 192.168.133.114 blocked due to potential attack"),
    ("BillingSystem", "User User12345 logged in"),
    ("LegacyCRM", "The 'ReportGenerator' module will be retired in version 4.0")
]

labels = classify(logs)
print(labels)  # Output: ['System Notification', 'User Action', 'Deprecation Warning']
```

## Troubleshooting

### Hugging Face Token Error
If you see warnings about unauthenticated requests:
```bash
huggingface-cli login
# or set environment variable:
set HF_TOKEN=your_token_here
```

### Model Not Found
Ensure the trained model exists at `Training/model/log_classifier.joblib`. The sentence transformer model will auto-download on first run.

### CSV Parsing Error
Ensure your CSV is properly formatted with:
- Correct headers: `source,log_message`
- Quoted fields containing commas
- Proper line endings

## Training

To retrain the BERT classifier:
1. Prepare labeled training data
2. Run the training script in `Training/` directory
3. Save the model as `Training/model/log_classifier.joblib`

## Performance Notes

- **Regex classifier**: ~0.1ms per log
- **BERT classifier**: ~10-50ms per log (GPU-accelerated)
- **LLM classifier**: ~500ms-2s per log (API dependent)

For batch processing, expect ~10-100 logs/second depending on the mix of classifiers used.

## License

MIT

## Author

Created for enterprise log classification and analysis.

## Contributing

Improvements welcome! Areas for enhancement:
- Add more regex patterns for additional log sources
- Retrain BERT model with more labeled data
- Optimize inference speed
- Add structured logging support (JSON logs)
- Implement confidence scoring per log
