from openai import OpenAI

def generate_embedding(text: str, api_key: str):
    try:
        client = OpenAI(api_key=api_key)
        response = client.embeddings.create(input=text, model="text-embedding-ada-002")
        return response.data[0].embedding
    except Exception as e:
        print(f"⚠️ Lỗi khi tạo embedding: {e}")
        return None