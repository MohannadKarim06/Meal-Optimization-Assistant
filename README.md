# AI-Powered Meal Optimization System

A sophisticated RAG (Retrieval-Augmented Generation) system that provides personalized meal recommendations and nutritional guidance based on intelligent document analysis and meal classification.

## 🚀 Features

### Core Functionality
- **Smart Meal Classification**: Automatically categorizes meals into 4 distinct types (A, B, C, D) based on nutritional profiles
- **Intelligent Query Processing**: Distinguishes between food queries, greetings, and general questions
- **Document-Based Recommendations**: Leverages uploaded PDF documents to provide contextual nutritional advice
- **Real-time Response Generation**: Fast, accurate responses powered by OpenAI's GPT models

### Technical Highlights
- **RAG Architecture**: Combines document retrieval with generative AI for contextually relevant responses
- **Vector Search**: FAISS-powered similarity search for efficient document chunk retrieval
- **Token Management**: Smart prompt building that respects model token limits
- **Scalable Design**: Modular pipeline architecture for easy maintenance and extension

## 🛠️ Technology Stack

- **Backend**: FastAPI (Python)
- **AI/ML**: OpenAI GPT models, OpenAI Embeddings
- **Vector Database**: FAISS (Facebook AI Similarity Search)
- **Document Processing**: PyMuPDF for PDF text extraction
- **Tokenization**: tiktoken for accurate token counting
- **Containerization**: Docker for deployment

## 📋 API Endpoints

### Core Endpoints
- `POST /ask` - Submit meal queries for optimization recommendations
- `POST /upload` - Upload PDF documents for knowledge base
- `GET /files` - List all uploaded documents
- `DELETE /delete/{filename}` - Remove documents and associated data

### Configuration & Monitoring
- `GET /config` - Retrieve current system configuration
- `POST /config` - Update system settings
- `GET /logs` - Access system logs for debugging

## 🏗️ Architecture

### Pipeline Components

1. **Query Pipeline**
   - Query type identification (food/greeting/other)
   - Meal type classification (A/B/C/D)
   - Document retrieval and ranking
   - Response generation with context

2. **File Pipeline**
   - PDF text extraction
   - Intelligent text chunking
   - Vector embedding generation
   - FAISS index creation and storage

3. **Supporting Systems**
   - Configuration management
   - Token limit handling
   - Query sanitization
   - Comprehensive logging

## 🚀 Quick Start

### Prerequisites
- Python 3.11+
- OpenAI API key
- Docker (optional)

### Installation

1. **Clone and Setup**
   ```bash
   git clone <repository-url>
   cd meal-optimization-system
   pip install -r requirements.txt
   ```

2. **Environment Configuration**
   ```bash
   export OPENAI_API_KEY="your-api-key-here"
   ```

3. **Run the Application**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

### Docker Deployment
```bash
docker build -t meal-optimizer .
docker run -e OPENAI_API_KEY="your-key" -p 8000:8000 meal-optimizer
```

## 📊 Configuration Options

The system supports dynamic configuration through `/config` endpoint:

```json
{
  "chat_model_name": "gpt-4-turbo",
  "embedding_model_name": "text-embedding-ada-002",
  "base_prompt": "You are a helpful assistant.",
  "top_k_results": 5,
  "token_limit": 8000,
  "similarity_threshold": 0.6
}
```

## 🔍 How It Works

### Meal Classification System
The system intelligently categorizes meals into four types based on their nutritional profile:
- **Type A**: High-glycemic foods, refined carbs, sugars, alcohol
- **Type B**: Moderate whole grains, legumes, balanced meals
- **Type C**: Protein-focused with non-starchy vegetables
- **Type D**: High-protein, low-carb, optimal choices

### Document Processing
1. PDFs are uploaded and processed section by section
2. Text is chunked intelligently to preserve context
3. Each chunk is embedded using OpenAI's embedding models
4. FAISS indexes enable fast similarity search

### Response Generation
1. User queries are classified and sanitized
2. Relevant document chunks are retrieved using vector search
3. Context is built within token limits
4. GPT generates personalized recommendations

## 📁 Project Structure

```
├── app/
│   ├── api/                 # OpenAI API integration
│   ├── pipelines/           # Core processing pipelines
│   ├── config.py           # System configuration
│   └── main.py             # FastAPI application
├── utils/
│   ├── config_handler.py   # Configuration management
│   ├── file_handler.py     # Document processing
│   ├── query_handler.py    # Query processing logic
│   ├── token_handler.py    # Token management
│   └── logger.py           # Logging utilities
├── data/                   # Data storage directories
├── requirements.txt        # Python dependencies
└── dockerfile             # Container configuration
```

## 🔧 Key Components

### FileHandler
- PDF text extraction with section awareness
- Intelligent chunking that preserves document structure
- FAISS index management for efficient retrieval

### QueryHandler
- Multi-stage query classification
- Query sanitization and validation
- Response generation with type-specific prompting

### TokenHandler
- Accurate token counting for multiple models
- Smart prompt building within limits
- Context optimization for better responses

## 📈 Performance Features

- **Efficient Search**: FAISS indexing for sub-second document retrieval
- **Smart Caching**: Processed documents stored for quick access
- **Token Optimization**: Automatic prompt truncation to fit model limits
- **Parallel Processing**: Concurrent document processing capabilities

## 🛡️ Security & Best Practices

- Environment-based API key management
- Input sanitization for all user queries
- Comprehensive error handling and logging
- File type validation for uploads

## 📝 Logging & Monitoring

The system provides detailed logging for:
- Query processing stages
- Document upload and processing
- Error tracking and debugging
- Performance metrics

## 🤝 Contributing

This system is designed with modularity in mind. Key areas for extension:
- Additional document formats (Word, text files)
- Enhanced meal classification algorithms
- Integration with other AI providers
- Advanced analytics and reporting

## 📊 Use Cases

- **Personal Nutrition**: Individual meal optimization
- **Healthcare Applications**: Dietary guidance systems
- **Fitness Platforms**: Nutrition coaching tools
- **Educational Systems**: Nutritional learning platforms

---

*Built with modern AI technologies to provide intelligent, contextual nutritional guidance through advanced document understanding and meal analysis.*
