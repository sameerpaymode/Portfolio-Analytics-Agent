### Description

This project is an AI-powered Portfolio Analytics Agent that can understand natural language questions related to portfolio data and automatically decide whether to query a SQL database or calculate portfolio exposure metrics. The solution includes a FastAPI backend for production-ready API access, a command-line interface for quick testing, and an interactive Streamlit UI for user-friendly exploration. The agent uses LLM-powered reasoning to convert user questions into SQL queries, calculate sector exposures, and return meaningful financial insights from portfolio holdings data.

### How to Run the Project

#### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

#### 2. Add Environment Variables

Create a `.env` file and add your API key:

```env
GEMINI_API_KEY = your_api_key_here
GEMINI_MODEL =  model name here

GROQ_API_KEY =  your_api_key_here
```

#### 3. Run the FastAPI Backend

```bash
python app.py
```

This starts the API server where the AI Portfolio Agent can process portfolio-related queries programmatically.

#### 4. Run the Streamlit UI

```bash
streamlit run streamlit_app.py
```

This launches an interactive web interface where users can directly ask portfolio-related questions in natural language.

#### 5. Example Questions

* “How many portfolios do we have?”
* “Show sector exposure for portfolio 101”
* “Which sector has the highest allocation?”
* “List all equity holdings in Growth Portfolio”

#### 6. Run Evaluation Script

```bash
python evaluator.py
```

This validates the agent’s responses against the provided ground truth dataset to measure accuracy and functionality.


