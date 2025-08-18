from typing import List
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams

from app.core.config import settings


def get_qdrant_client() -> QdrantClient:
    """
    Get Qdrant client instance.

    Returns:
        QdrantClient: Configured Qdrant client
    """
    if settings.QDRANT_API_KEY:
        return QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
            api_key=settings.QDRANT_API_KEY,
        )
    else:
        return QdrantClient(
            host=settings.QDRANT_HOST,
            port=settings.QDRANT_PORT,
        )


def init_qdrant_collection(
    client: QdrantClient, collection_name: str = None
) -> None:
    """
    Initialize Qdrant collection if it doesn't exist.

    Args:
        client: Qdrant client instance
        collection_name: Name of the collection (defaults to settings value)
    """
    collection_name = collection_name or settings.QDRANT_COLLECTION_NAME

    # Check if collection exists
    collections = client.get_collections()
    collection_names = [col.name for col in collections.collections]

    if collection_name not in collection_names:
        # Create collection with vector configuration
        # Using 384 dimensions for FastEmbed embeddings (consistent with dr_ubyfol)
        client.create_collection(
            collection_name=collection_name,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )


def init_enem_collections(client: QdrantClient) -> None:
    """
    Initialize ENEM-specific collections for knowledge base.
    
    Args:
        client: Qdrant client instance
    """
    # ENEM subjects for specialized collections
    enem_subjects = [
        'matematica',
        'portugues',
        'literatura',
        'ingles',
        'espanhol', 
        'fisica',
        'quimica',
        'biologia',
        'historia',
        'geografia',
        'filosofia',
        'sociologia',
        'redacao'
    ]
    
    # Get existing collections
    collections = client.get_collections()
    collection_names = [col.name for col in collections.collections]
    
    # Create main ENEM knowledge collection (unified approach)
    main_collection = settings.QDRANT_COLLECTION_NAME
    if main_collection not in collection_names:
        client.create_collection(
            collection_name=main_collection,
            vectors_config=VectorParams(size=384, distance=Distance.COSINE),
        )
    
    # Optionally create subject-specific collections
    for subject in enem_subjects:
        collection_name = f"enem-{subject}"
        if collection_name not in collection_names:
            client.create_collection(
                collection_name=collection_name,
                vectors_config=VectorParams(size=384, distance=Distance.COSINE),
            )


def get_enem_subjects() -> List[str]:
    """
    Get list of ENEM subjects for knowledge organization.
    
    Returns:
        List of ENEM subject identifiers
    """
    return [
        'matematica',
        'portugues',
        'literatura', 
        'ingles',
        'espanhol',
        'fisica',
        'quimica',
        'biologia',
        'historia',
        'geografia',
        'filosofia',
        'sociologia',
        'redacao'
    ]
