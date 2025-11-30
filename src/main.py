import os
from dotenv import load_dotenv

from graph import build_graph
from state import PipelineState

def main():
    # Load .env if present
    if os.path.exists(".env"):
        load_dotenv()

    print("🧠 AI Data Pipeline Design Assistant (LangGraph + Claude)")
    print("------------------------------------------------------------------")
    print("Describe your data pipeline scenario in one or more sentences.")
    print("Example:")
    print("  I have CSV files in Azure Blob (~200GB/day) and want a Delta Lake")
    print("  on Databricks with bronze/silver/gold layers and Power BI on top.")
    print("------------------------------------------------------------------")

    user_query = input("Describe your data pipeline scenario:\n> ").strip()
    if not user_query:
        print("No input provided. Exiting.")
        return

    state: PipelineState = {"user_query": user_query}

    app = build_graph()
    final_state = app.invoke(state)

    print("\n================= PIPELINE DESIGN RESULT =================\n")
    print(final_state.get("final_answer", "No answer generated. Check logs."))

if __name__ == "__main__":
    main()
