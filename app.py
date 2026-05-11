from fastapi import FastAPI
from pydantic import BaseModel

from src.portfolioagent import PortfolioAgent

app = FastAPI(
    title="Portfolio AI Agent",
    version="1.0.0"
)

agent = PortfolioAgent()

class QuestionRequest(BaseModel):
    question: str

from fastapi.responses import FileResponse

@app.get("/")
def serve_ui():
    return FileResponse("static/index.html")


@app.post("/ask")
def ask_agent(request: QuestionRequest):

    response = agent.answer_question(
        question=request.question
    )


    usage = response.usage_metadata

    token_usage = {
        "prompt_tokens": usage.prompt_token_count,
        "completion_tokens": usage.candidates_token_count,
        "total_tokens": usage.total_token_count
    }

    tool_calls = []

    history = response.automatic_function_calling_history

    if history:

        for item in history:

            # Tool requested by model
            if item.role == "model":

                for part in item.parts:

                    if getattr(part, "function_call", None):

                        tool_calls.append({
                            "tool_name": part.function_call.name,
                            "arguments": dict(
                                part.function_call.args
                            )
                        })

            # Tool response
            elif item.role == "user":

                for part in item.parts:

                    if getattr(part, "function_response", None):

                        if tool_calls:

                            tool_calls[-1]["response"] = (
                                part.function_response.response
                            )

    return {
        "response": response.text,

        "model": response.model_version,

        "tokens": token_usage,

        "tool_calls": tool_calls
    }

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        "app:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )