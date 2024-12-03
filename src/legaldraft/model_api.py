from fastapi import FastAPI, HTTPException
import uvicorn 
from pydantic import BaseModel
from dotenv import load_dotenv
import os
import litellm
from crew import Legaldraft

# Load environment variables from .env file
load_dotenv()

app = FastAPI()

class QueryRequest(BaseModel):
    query_text: str


@app.get('/')
def root():
    return {"Hello": "World"}

@app.post("/submit_query")
def submit_query_endpoint(request: QueryRequest):
    try:
        # Retrieve API key from environment variable
        openai_api_key = os.getenv('OPENAI_API_KEY')
        
        # Check if API key is present
        if not openai_api_key:
            raise HTTPException(
                status_code=401, 
                detail="OpenAI API key is not configured"
            )

        # Explicitly set the API key
        os.environ['OPENAI_API_KEY'] = openai_api_key
        litellm.api_key = openai_api_key

        # Proceed with your existing logic
        inputs = {'topic': request.query_text}
        result = Legaldraft().crew().kickoff(inputs=inputs)
        return {"result":result}
    
    except litellm.AuthenticationError as auth_error:
        raise HTTPException(
            status_code=401, 
            detail=f"Authentication failed: {str(auth_error)}"
        )
    except Exception as e:
        raise HTTPException(
            status_code=500, 
            detail=f"An unexpected error occurred: {str(e)}"
        )
    
if __name__== "__main__":
    port=5000
    print(f"Running the fastAPI server on port {port}.")
    uvicorn.run(app,host="127.0.0.1",port=port)
