from fastapi import FastAPI, Body
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import os
from dotenv import load_dotenv
import weaviate
from langchain.embeddings import CohereEmbeddings
from langchain.vectorstores import Weaviate
from langchain.llms import OpenAI
from langchain.chains import RetrievalQA

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')
cohere_api_key = os.getenv('COHERE_API_KEY')
weaviate_api_key = os.getenv('weaviate_api_key')
weaviate_url = os.getenv('weaviate_url')

auth_config = weaviate.auth.AuthApiKey(api_key=weaviate_api_key) 

client = weaviate.Client( url=weaviate_url, auth_client_secret=auth_config, 
                         additional_headers={ "X-Cohere-Api-Key": cohere_api_key})
vectorstore = Weaviate(client,  index_name="Articles", text_key="text")
vectorstore._query_attrs = ["text", "title", "url", "views", "lang", "_additional {distance}"]
vectorstore.embedding =CohereEmbeddings(model="embed-multilingual-v2.0", cohere_api_key=cohere_api_key)
llm =OpenAI(temperature=0, openai_api_key=openai_api_key)
qa = RetrievalQA.from_chain_type(llm, retriever=vectorstore.as_retriever())

class ChatRequest(BaseModel):
    query: str

@app.post("/chat")
async def chat_resp(request: ChatRequest = Body(...)):
    query = request.query
    result = qa({"query": query})
    return result['result']
