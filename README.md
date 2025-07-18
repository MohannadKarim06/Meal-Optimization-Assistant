# Meal Optimization Assistant

A FastAPI-based application that helps users optimize their meals for better blood glucose response while maintaining flavor. The system uses OpenAI's GPT models and a RAG (Retrieval-Augmented Generation) approach to provide personalized meal optimization suggestions.

## Features

- **Meal Analysis**: Classifies meals into different types (A, B, C, D) based on their glucose impact
- **Smart Query Handling**: Distinguishes between new food queries, greetings, follow-ups, and other requests
- **Document Processing**: Upload and process PDF documents containing meal optimization guidelines
- **Vector Search**: Uses FAISS for semantic search through uploaded documents
- **Chat History**: Maintains conversation context for better follow-up responses
- **Admin Interface**: Streamlit-based admin panel for file management and configuration
- **User Interface**: Clean Streamlit interface for asking questions

## Architecture

### Core Components

- **FastAPI Backend**: Main API server handling requests and business logic
- **OpenAI Integration**: GPT models for text generation and embeddings
- **FAISS Vector Store**: Efficient similarity search for document chunks
- **Streamlit UIs**: Admin dashboard and user interface
- **Docker Support**: Containerized deployment

### Project Structure

```
├── app/
│   ├── api/
│   │   └── openai_client.py          # OpenAI API integration
│   ├── pipelines/
│   │   ├── file_pipeline.py          # Document processing pipeline
│   │   └── query_pipeline.py         # Query processing pipeline
│   ├── config.py                     # Configuration constants
│   └── main.py                       # FastAPI application
├── utils/
│   ├── config_handler.py             # Configuration management
│   ├── file_handler.py               # PDF processing and vector operations
│   ├── logger.py                     # Logging utilities
│   ├── query_handler.py              # Query classification and handling
│   └── token_handler.py              # Token counting and management
├── UIs/
│   ├── Admin UI/                     # Streamlit admin interface
│   └── Ask UI/                       # Streamlit user interface
├── .github/workflows/
│   └── fly-deploy.yml                # GitHub Actions deployment
├── dockerfile                        # Main application container
├── fly.toml                          # Fly.io deployment configuration
└── requirements.txt                  # Python dependencies
```

## Installation

### Prerequisites

- Python 3.9+
- Docker (optional)
- OpenAI API key

### Local Development

1. **Clone the repository**
   ```bash
   git clone <repository-url>
   cd meal-optimization-assistant
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set environment variables**
   ```bash
   export OPENAI_API_KEY="your-openai-api-key"
   export API_BASE="http://localhost:8000"  # For UIs
   ```

4. **Run the FastAPI server**
   ```bash
   uvicorn app.main:app --host 0.0.0.0 --port 8000
   ```

5. **Run the Streamlit UIs** (in separate terminals)
   ```bash
   # Admin UI
   cd UIs/Admin\ UI
   streamlit run src/streamlit_app.py --server.port=8501

   # Ask UI
   cd UIs/Ask\ UI
   streamlit run src/streamlit_app.py --server.port=8502
   ```

### Docker Deployment

1. **Build and run with Docker**
   ```bash
   docker build -t meal-optimization-assistant .
   docker run -p 8000:8000 -e OPENAI_API_KEY="your-key" meal-optimization-assistant
   ```

2. **Or use docker-compose** (create a docker-compose.yml file)
   ```yaml
   version: '3.8'
   services:
     api:
       build: .
       ports:
         - "8000:8000"
       environment:
         - OPENAI_API_KEY=your-openai-api-key
       volumes:
         - ./data:/app/data
   ```

## Usage

### API Endpoints

- `GET /` - Health check
- `POST /ask` - Ask a question about meal optimization
- `POST /upload` - Upload PDF documents
- `DELETE /delete/{filename}` - Delete uploaded files
- `GET /files` - List uploaded files
- `GET /config` - Get configuration
- `POST /config` - Update configuration
- `GET /logs` - View application logs

### Meal Classification

The system classifies meals into four types:

- **Type A**: High glucose impact (refined grains, sugars, alcohol)
- **Type B**: Moderate impact (whole grains, legumes, dairy)
- **Type C**: Lower impact (protein with vegetables)
- **Type D**: Minimal impact (pure protein, non-starchy vegetables)

### Query Types

1. **New Food Queries**: Specific meals/beverages to optimize
2. **Greetings**: Welcome messages
3. **Follow-ups**: Questions about previous recommendations
4. **Other**: General questions not about specific foods

## Configuration

The application uses a JSON configuration file with the following settings:

```json
{
  "chat_model_name": "gpt-4-turbo",
  "embedding_model_name": "text-embedding-ada-002",
  "base_prompt": "System prompt for meal optimization",
  "top_k_results": 5,
  "token_limit": 8000,
  "follow_ups_prompt": "Prompt for follow-up questions",
  "type_d_limit": false,
  "follow_ups_limit": true
}
```

## Deployment

### Fly.io Deployment

The project is configured for deployment on Fly.io:

1. **Install Fly CLI**
   ```bash
   curl -L https://fly.io/install.sh | sh
   ```

2. **Login and deploy**
   ```bash
   fly auth login
   fly deploy
   ```

3. **Set secrets**
   ```bash
   fly secrets set OPENAI_API_KEY="your-openai-api-key"
   ```

### GitHub Actions

Automatic deployment is configured via GitHub Actions. Push to the `main` branch triggers deployment.

## Document Processing

1. **Upload PDFs** through the admin interface
2. **Text Extraction** using PyMuPDF
3. **Chunking** by sections marked with "Section: " headers
4. **Embedding** using OpenAI's text-embedding-ada-002
5. **Indexing** with FAISS for fast similarity search

## Logging

All operations are logged with different levels:
- `PROCESS`: Operation start notifications
- `SUCCESS`: Successful completion
- `ERROR`: Error conditions
- `INFO`: General information

View logs through the admin interface or the `/logs` endpoint.

## Environment Variables

- `OPENAI_API_KEY`: Required for OpenAI API access
- `API_BASE`: Base URL for the API (used by UIs)
- `STREAMLIT_TELEMETRY`: Set to "0" to disable telemetry
- `STREAMLIT_DISABLE_USAGE_STATS`: Set to "true" to disable usage stats

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions, please [create an issue](link-to-issues) in the repository.

## Acknowledgments

- OpenAI for GPT models and embeddings
- FastAPI for the web framework
- Streamlit for the user interfaces
- FAISS for vector similarity search
