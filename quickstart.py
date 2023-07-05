#%%
import weaviate
import json

client = weaviate.Client(
    url = "https://some-endpoint.weaviate.network",  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key="YOUR-WEAVIATE-API-KEY"),  # Replace w/ your Weaviate instance API key
    additional_headers = {
        "X-HuggingFace-Api-Key": "YOUR-HUGGINGFACE-API-KEY"  # Replace with your inference API key
    }
)