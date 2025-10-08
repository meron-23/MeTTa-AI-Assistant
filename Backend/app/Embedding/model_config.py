from sentence_transformers import SentenceTransformer

# Load and cache the embedding model (with dependency injection)
def get_embedding_model(model_loader=SentenceTransformer, model_name="all-MiniLM-L6-v2"):
    """
    Load and return an embedding model using dependency injection.
    The model_loader (dependency) is injected from outside.
    """
    print(f"Loading embedding model: {model_name}")
    return model_loader(model_name)
