import os
from langchain.embeddings.openai import OpenAIEmbeddings
from dotenv import load_dotenv
import pinecone
import uuid

load_dotenv()
api_key = os.getenv("PINE_CONE_API")

pinecone.init(api_key=api_key, environment="asia-southeast1-gcp-free")


def generate_identifier():
    identifier = str(uuid.uuid4())[:5]
    return identifier


def embed_text(text: str):
    embeddings = OpenAIEmbeddings()
    query_result = embeddings.embed_query(text)
    id = generate_identifier()
    index = pinecone.Index("aipodcasts")
    # index = pinecone.GRPCIndex("aipodcasts")
    index.upsert([{"id": id, "values": query_result}])
    return id, query_result


def get_vector_by_id(vector_id):
    # Get the vector using the ID
    index = pinecone.Index("aipodcasts")
    fetch_response = index.fetch(ids=vector_id)
    print(fetch_response['vectors'][vector_id[0]]['values'])
    return fetch_response

# print(embed_text("Hello World"))
# print(len(embed_text("Hello World")))
