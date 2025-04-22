import agent_config
from fastapi import FastAPI
from model import UserQuery
from fastapi.responses import JSONResponse
from fastapi import FastAPI, UploadFile, File
from utils import extract_chunks_from_pdf, insert_chunks_into_milvus


app = FastAPI()

@app.post("/conversation")
async def conversation(payload: UserQuery):
    """
    Endpoint to handle conversation with the agent.
    """
    if "research" in payload.query:
        # Use the deep research agent for research queries
        agent_name = agent_config.internal_search_agent
    else:
        # Use the web search agent for other queries
        agent_name = agent_config.web_search_agent

    # Call the agent asynchronously
    result = await agent_config.call_agent_async(agent_name, payload.query)
    return JSONResponse(content={"response": result.response})

@app.post("/upload-file")
async def upload_pdf(file: UploadFile = File(...)):
    file_bytes = await file.read()
    chunks = extract_chunks_from_pdf(file_bytes)
    insert_chunks_into_milvus(chunks)
    return {"message": "PDF processed and stored in Milvus!"}


if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app
    uvicorn.run(app, host="127.0.1", port=8080)
