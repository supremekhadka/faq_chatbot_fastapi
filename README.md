# FAQ Chatbot API

This is a FastAPI-based chatbot application that answers questions based on a predefined set of FAQs using natural language processing and semantic search technology.

## Features

- **FastAPI Backend**: Provides a robust and efficient API for handling chatbot requests.
- **Semantic Search**: Uses sentence embeddings to find the most relevant answers.
- **Pre-trained Model**: Uses `all-MiniLM-L6-v2` model for high-quality text embeddings.
- **Confidence Scoring**: Returns similarity scores to indicate answer confidence.
- **Dockerized Deployment**: Simplified deployment and consistency across environments.
- **Configurable**: Easily adjustable settings through environment variables.

## Getting Started

### Prerequisites

- Python 3.8+
- pip
- Docker

### Installation

1.  Clone the repository:

    ```bash
    git clone <repository_url>
    cd faq_chatbot_fastapi
    ```

2.  Create a virtual environment:

    ```bash
    python -m venv venv
    source venv/bin/activate  # On Linux/macOS
    venv\Scripts\activate    # On Windows
    ```

3.  Install the dependencies:

    ```bash
    pip install -r requirements.txt
    ```

### Usage

1.  Run the FastAPI application:

    ```bash
    uvicorn app.main:app --reload
    ```

    This will start the server at http://localhost:8000.

    Access the FastAPI Swagger UI at http://localhost:8000/docs to make API calls from the webpage.

2.  Test the API endpoint by sending a POST request to http://localhost:8000/api/v1/query:

    ```bash
    curl -X POST "http://localhost:8000/api/v1/query" \
        -H "Content-Type: application/json" \
        -d '{"query": "What are your business hours?"}'
    ```

    Example response:

    ```json
    {
      "matched_question": "What are your business hours?",
      "answer": "Our business hours are Monday to Friday, 9 AM to 6 PM.",
      "score": 0.92,
      "message": null
    }
    ```

### Docker Deployment

1.  Build the Docker image:

    ```bash
    docker build -t faq_chatbot .
    ```

2.  Run the Docker container:

    ```bash
    docker run -p 8000:8000 faq_chatbot
    ```

    The application will be accessible at http://localhost:8000.

### Configuration

The application can be configured using environment variables. The following variables are supported:

- `SENTENCE_TRANSFORMER_MODEL`: Model to use for embeddings (default: "all-MiniLM-L6-v2")
- `SIMILARITY_THRESHOLD`: Minimum similarity score to return an answer (default: 0.5)

### API Endpoints

#### GET /

Root endpoint returning a welcome message.

#### POST /api/v1/query

Submit a question to the chatbot.

**Request Body**:

```json
{
  "query": "string"
}
```

### Responses:

- **200 OK**: Successfully processed query

  ```json
  {
    "matched_question": "string",
    "answer": "string",
    "score": 0.0,
    "message": "string"
  }
  ```

- **400 Bad Request**: Empty query

- **500 Internal Server Error**: Server error

### FAQ Data Format

The FAQ data is stored in JSON format:

```json
[
  {
    "id": 1,
    "question": "What are your business hours?",
    "answer": "Our business hours are Monday to Friday, 9 AM to 6 PM."
  },
  {
    "id": 2,
    "question": "How can I reset my password?",
    "answer": "You can reset your password by clicking the 'Forgot Password' link on the login page."
  }
]
```

## Contributing

Contributions are welcome! Please submit a pull request with your changes.

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Project Layout

```bash
faq_chatbot_fastapi/
├── app/
│   ├── __init__.py
│   ├── main.py
│   ├── api/
│   │   ├── __init__.py
│   │   └── chatbot.py
│   ├── core/
│   │   ├── __init__.py
│   │   └── config.py
│   ├── services/
│   │   ├── __init__.py
│   │   └── faq_service.py
│   └── models/
│       ├── __init__.py
│       └── chatbot_models.py
├── tests/
│   ├── __init__.py
│   └── test_chatbot_api.py
├── data/
│   └── faqs.json
├── .env.example
├── .gitignore
├── Dockerfile
├── docker-compose.yml
├── LICENSE
├── README.md
├── mkdocs.yml
├── docs/
├── requirements.txt
├── requirements-dev.txt
└── pyproject.toml
```
