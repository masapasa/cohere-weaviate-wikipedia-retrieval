# %% [markdown]
# ## Dependencies

# %%
!pip install weaviate-client

# %% [markdown]
# ## Configuration

# %%
import weaviate
import json
WEAVIATE-INSTANCE-URL = os.getenv('weaviate_url')
AUTH-KEY = os.getenv('weaviate_api_key')
OPENAI-API-KEY = os.getenv('OPENAI_API_KEY')
client = weaviate.Client(
  url="WEAVIATE-INSTANCE-URL",  # URL of your Weaviate instance
  auth_client_secret=weaviate.AuthApiKey(api_key="AUTH-KEY"), # (Optional) If the Weaviate instance requires authentication
  additional_headers={
    "X-OpenAI-Api-Key": "OPENAI-API-KEY", # Replace with your OpenAI key
  }
)

client.schema.get()  # Get the schema to test connection

# %% [markdown]
# ## Schema

# %%
# resetting the schema. CAUTION: THIS WILL DELETE YOUR DATA 
client.schema.delete_all()

schema = {
   "classes": [
       {
           "class": "JeopardyQuestion",
           "description": "List of jeopardy questions",
           "vectorizer": "text2vec-openai",
           "moduleConfig": { # specify the model you want to use
               "generative-openai": { 
                    "model": "gpt-3.5-turbo",  # Optional - Defaults to `gpt-3.5-turbo`
                }
           },
           "properties": [
               {
                  "name": "Category",
                  "dataType": ["text"],
                  "description": "Category of the question",
               },
               {
                  "name": "Question",
                  "dataType": ["text"],
                  "description": "The question",
               },
               {
                  "name": "Answer",
                  "dataType": ["text"],
                  "description": "The answer",
                }
            ]
        }
    ]
}

client.schema.create(schema)

print("Successfully created the schema.")

# %% [markdown]
# ## Import the Data

# %%
import requests
url = 'https://raw.githubusercontent.com/weaviate/weaviate-examples/main/jeopardy_small_dataset/jeopardy_tiny.json'
resp = requests.get(url)
data = json.loads(resp.text)

if client.is_ready():

# Configure a batch process
  with client.batch as batch:
      batch.batch_size=100
      # Batch import all Questions
      for i, d in enumerate(data):
          print(f"importing question: {i+1}")

          properties = {
              "answer": d["Answer"],
              "question": d["Question"],
              "category": d["Category"],
          }

          client.batch.add_data_object(properties, "JeopardyQuestion")
else:
  print("The Weaviate cluster is not connected.")

# %% [markdown]
# ## Generative Search Queries

# %% [markdown]
# ### Single Result

# %% [markdown]
# Single Result makes a generation for each individual search result. 
# 
# In the below example, I want to create a Facebook ad from the Jeopardy question about Elephants. 

# %%
generatePrompt = "Turn the following Jeogrady question into a Facebook Ad: {question}"

result = (
  client.query
  .get("JeopardyQuestion", ["question"])
  .with_generate(single_prompt = generatePrompt)
  .with_near_text({
    "concepts": ["Elephants"]
  })
  .with_limit(1)
).do()

print(json.dumps(result, indent=1))

# %% [markdown]
# ### Grouped Result

# %% [markdown]
# Grouped Result generates a single response from all the search results. 
# 
# The below example is creating a Facebook ad from the 3 retrieved Jeoprady questions about animals. 

# %%
generateTask = "Explain why these Jeopardy questions are under the Animals category."

result = (
  client.query
  .get("JeopardyQuestion", ["question"])
  .with_generate(grouped_task = generateTask)
  .with_near_text({
    "concepts": ["Animals"]
  })
  .with_limit(3)
).do()

print(json.dumps(result, indent=1))


