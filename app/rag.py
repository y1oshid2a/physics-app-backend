import os
import chromadb
from anthropic import Anthropic
from sentence_transformers import SentenceTransformer
from dotenv import load_dotenv

load_dotenv()

client = Anthropic()
embedding_model = SentenceTransformer('all-MiniLM-L6-v2')
chroma_client = chromadb.PersistentClient(path="./chroma_db")
collection = chroma_client.get_or_create_collection("physics")

def load_and_index_document(filepath: str):
    with open(filepath, 'r', encoding='utf-8') as f:
        text = f.read()

    chunks = [c.strip() for c in text.split('\n\n') if c.strip()]

    embeddings = embedding_model.encode(chunks).tolist()

    collection.upsert(
        documents=chunks,
        embeddings=embeddings,
        ids=[f"chunk_{i}" for i in range(len(chunks))]
    )
    return len(chunks)

def search_relevant_chunks(query: str, n_results: int = 3) -> list[str]:
    query_embedding = embedding_model.encode([query]).tolist()
    results = collection.query(
        query_embeddings=query_embedding,
        n_results=n_results
    )
    return results['documents'][0]

def get_ai_answer(question_title: str, question_content: str) -> str:
    relevant_chunks = search_relevant_chunks(question_content)
    context = '\n\n'.join(relevant_chunks)

    message = client.messages.create(
        model="claude-sonnet-4-5",
        max_tokens=1024,
        messages=[
            {
                "role": "user",
                "content": f"""あなたは物理の先生です。以下の教材を参考にして、生徒の質問に答えてください。

【参考教材】
{context}

【質問タイトル】
{question_title}

【質問内容】
{question_content}

丁寧でわかりやすい説明をお願いします。"""
            }
        ]
    )
    return message.content[0].text