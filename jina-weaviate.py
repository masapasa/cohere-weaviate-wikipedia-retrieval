from jina import DocumentArray, Flow
from weaviate_executor import WeaviateIndexer

# define data to be indexed
data = [
    {'text': 'This is document one'},
    {'text': 'This is document two'},
    {'text': 'This is document three'}
]

# create DocumentArray to hold data
docs = DocumentArray(
    [doc for doc in data]
)

# define a Weaviate Indexer executor
weaviate_indexer = WeaviateIndexer(
    property_mappings={
        "text": "string"             # specify mapping for 'text' field to map to Weaviate string property
    },
    weaviate_config={                   # specify Weaviate server endpoint and credentials
        'host': 'http://localhost:8080',
        'api_key': 'my-api-key'
    }
)

# create a Flow to index data and store in Weaviate
with Flow().add(weaviate_indexer) as f:
    f.index(inputs=docs)