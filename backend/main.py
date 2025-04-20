from agent_config import call_agent_async
from fastapi import FastAPI
from model import UserQuery
from fastapi.responses import JSONResponse



app = FastAPI()

@app.post("/conversation")
async def conversation(payload: UserQuery):
    """
    Endpoint to handle conversation with the agent.
    """
    # Call the agent asynchronously
    result = await call_agent_async(payload.query)
    return JSONResponse(content={"response": result.response})


if __name__ == "__main__":
    import uvicorn
    # Run the FastAPI app
    uvicorn.run(app, host="127.0.1", port=8000)
