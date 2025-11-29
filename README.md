# AI Data Pipeline Design Assistant (LangGraph + Claude)

This project is a **CLI-based AI assistant** that designs cloud + Spark data pipelines using
**LangGraph** for orchestration and **Claude** (Anthropic) as the LLM.

You can describe your source → target systems, workload type, and any constraints.
The assistant will generate:

- A proposed **pipeline architecture** (Azure / AWS)
- **PySpark / Databricks** starter code
- **IAM & access control** design suggestions
- **Cost & performance optimization** tips

All reasoning is broken into nodes using LangGraph:
- Input parsing
- Architecture planning
- Code generation
- IAM design
- Cost & performance advice
- Final answer composition

## 1. Prerequisites

- Python 3.10 or later
- A terminal / command prompt (VS Code integrated terminal is perfect)
- An **Anthropic API key** (for Claude)

Sign up for Anthropic and create an API key, then export it as an environment variable:

```bash
# Linux / macOS
export ANTHROPIC_API_KEY="your_api_key_here"

# Windows PowerShell
setx ANTHROPIC_API_KEY "your_api_key_here"
```

Or create a `.env` file (see `.env.example`) and use any env-loader you like.

## 2. Setup (VS Code friendly)

1. **Create and activate a virtual environment**

   ```bash
   cd pipeline_architect

   # Windows
   python -m venv .venv
   .venv\Scripts\activate

   # macOS / Linux
   # python3 -m venv .venv
   # source .venv/bin/activate
   ```

2. **Install dependencies**

   ```bash
   pip install -r requirements.txt
   ```

3. **Set your Anthropic API key**

   Make sure `ANTHROPIC_API_KEY` is available in your environment.

## 3. Run the assistant

From inside the virtual environment:

```bash
python main.py
```

You’ll be prompted:

```text
Describe your data pipeline scenario:
> I have CSV files landing in Azure Blob (~200GB/day), want to build a bronze-silver-gold Delta Lake in Databricks and expose curated tables to Power BI. Daily batch is fine, but we have customer PII.
```

The app will:

1. Parse your description
2. Plan a cloud architecture
3. Generate PySpark / Databricks starter code
4. Propose IAM / access setup
5. Provide cost & performance tips
6. Print a consolidated answer in the terminal

## 4. Project structure

```text
pipeline_architect/
├── main.py                # CLI entrypoint
├── graph.py               # LangGraph workflow definition
├── state.py               # PipelineState TypedDict
├── llm.py                 # Claude client helper
├── nodes/
│   ├── __init__.py
│   ├── input_parser.py
│   ├── architecture_planner.py
│   ├── code_generator.py
│   ├── iam_designer.py
│   ├── cost_perf_advisor.py
│   └── answer_composer.py
├── requirements.txt
├── .env.example
└── README.md
```

## 5. Customizing for the hackathon

- Add more nodes (e.g., **Data Quality Planner**, **Monitoring & Alerting Designer**).
- Swap the CLI for a **FastAPI** or **Streamlit** UI if you want a web demo.
- Extend `PipelineState` and prompts in `nodes/*` for more detailed outputs.
- Implement **looping / clarification** by asking follow-up questions and re-running the graph.

Enjoy building your LangGraph + Claude data pipeline architect! 🚀

## 6. FastAPI API server

You can also run this assistant as a **FastAPI** service.

### 6.1 Start the server

Make sure your virtual environment is activated and dependencies are installed:

```bash
uvicorn api:app --reload
```

By default this starts the server on `http://127.0.0.1:8000`.

- Open docs: `http://127.0.0.1:8000/docs`
- Health/root: `GET /` → basic message
- Main endpoint: `POST /design`

### 6.2 Example request (via `curl`)

```bash
curl -X POST "http://127.0.0.1:8000/design" \
     -H "Content-Type: application/json" \
     -d "{
           \"description\": \"I have CSV files in Azure Blob (~200GB/day) and want a Delta Lake on Databricks with bronze/silver/gold layers and Power BI on top. Daily batch is fine, we have customer PII.\"
         }"
```

The response will contain:

- `final_answer` – markdown combined result
- `architecture` – architecture-only text
- `pyspark_code` – generated PySpark / Databricks starter code
- `iam_design` – IAM / access control plan
- `cost_tips`, `performance_tips` – optimization guidance
