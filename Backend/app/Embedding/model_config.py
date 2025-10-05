from sentence_transformers import SentenceTransformer

# Load and cache the embedding model
def get_embedding_model():
   
    model_name = "all-MiniLM-L6-v2"
    print(f"Loading embedding model: {model_name}")
    return SentenceTransformer(model_name)
