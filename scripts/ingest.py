
import os
import sys
from langchain_community.document_loaders import TextLoader
from langchain.text_splitter import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
from qdrant_client import QdrantClient, models
import uuid

# Add project root to Python path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from app.core.config import settings

DATA_PATH = "data/"
COLLECTION_NAME = "enem_content"

def main():
    print("Starting data ingestion process...")

    # 1. Initialize clients
    qdrant_client = QdrantClient(host=settings.qdrant_host, port=settings.qdrant_port)
    embedding_model = SentenceTransformer('all-MiniLM-L6-v2')

    # 2. Load and process documents
    documents = []
    for filename in os.listdir(DATA_PATH):
        if filename.endswith(".md") or filename.endswith(".txt"):
            loader = TextLoader(os.path.join(DATA_PATH, filename))
            documents.extend(loader.load())
    
    if not documents:
        print("No documents found in the data directory. Exiting.")
        return

    text_splitter = RecursiveCharacterTextSplitter(chunk_size=1000, chunk_overlap=200)
    chunks = text_splitter.split_documents(documents)

    print(f"Loaded {len(documents)} document(s) and split into {len(chunks)} chunks.")

    # 3. Generate embeddings
    print("Generating embeddings for all chunks...")
    embeddings = embedding_model.encode([chunk.page_content for chunk in chunks])
    print("Embeddings generated.")

    # 4. Setup Qdrant collection
    qdrant_client.recreate_collection(
        collection_name=COLLECTION_NAME,
        vectors_config=models.VectorParams(
            size=embedding_model.get_sentence_embedding_dimension(),
            distance=models.Distance.COSINE
        )
    )
    print(f"Qdrant collection '{COLLECTION_NAME}' created or recreated.")

    # 5. Upload to Qdrant
    qdrant_client.upload_points(
        collection_name=COLLECTION_NAME,
        points=[
            models.PointStruct(
                id=str(uuid.uuid4()),
                vector=vector.tolist(),
                payload={"text": chunk.page_content, "metadata": chunk.metadata}
            )
            for chunk, vector in zip(chunks, embeddings)
        ]
    )

    print("Successfully uploaded points to Qdrant.")
    print("Ingestion process finished.")

if __name__ == "__main__":
    main()
