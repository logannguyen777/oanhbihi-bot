from openai import OpenAI
from services.openai_client import get_openai_client

def generate_embedding(text: str, api_key: str):
    try:
        
        client = get_openai_client(db)
        response = client.embeddings.create(input=text, model="text-embedding-ada-002")
        return response.data[0].embedding
    except Exception as e:
        print(f"⚠️ Lỗi khi tạo embedding: {e}")
        return None