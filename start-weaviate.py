import weaviate
import json

client = weaviate.Client(
    url = "https://some-endpoint.weaviate.network",  # Replace with your endpoint
    auth_client_secret=weaviate.AuthApiKey(api_key="YOUR-WEAVIATE-API-KEY"),  # Replace w/ your Weaviate instance API key
    additional_headers = {
        "X-HuggingFace-Api-Key": "YOUR-HUGGINGFACE-API-KEY"  # Replace with your inference API key
    }
)

# ===== add schema =====
class_obj = {
    "class": "Question",
    "vectorizer": "text2vec-huggingface",  # If set to "none" you must always provide vectors yourself. Could be any other "text2vec-*" also.
    "moduleConfig": {
        "text2vec-huggingface": {
            "model": "sentence-transformers/all-MiniLM-L6-v2",  # Can be any public or private Hugging Face model.
            "options": {
                "waitForModel": True
            }
        }
    }
}

client.schema.create_class(class_obj)

# ===== import data =====
# Load data
import requests
url = 'https://raw.githubusercontent.com/weaviate-tutorials/quickstart/main/data/jeopardy_tiny.json'
resp = requests.get(url)
data = json.loads(resp.text)

# Configure a batch process
with client.batch(
    batch_size=100
) as batch:
    # Batch import all Questions
    for i, d in enumerate(data):
        print(f"importing question: {i+1}")

        properties = {
            "answer": d["Answer"],
            "question": d["Question"],
            "category": d["Category"],
        }

        client.batch.add_data_object(
            properties,
            "Question",
        )