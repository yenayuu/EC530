from fastapi import FastAPI, Form
from fastapi.middleware.cors import CORSMiddleware
from llm_service import get_llm_response

app = FastAPI()

# Allow frontend to access backend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.post("/analyze/")
async def analyze(task: str = Form(...), content: str = Form(...)):
    result = get_llm_response(task, content)
    return {"result": result}
