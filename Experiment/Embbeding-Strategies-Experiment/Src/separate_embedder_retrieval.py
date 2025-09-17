import numpy as np
import torch
import json
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class InteractiveGoogleEmbedderRetrieval:
    def __init__(self):
        self.model = None
        self.functions = None
        self.code_embeddings = {}  # Dictionary to store code embeddings with an ID
        self.desc_embeddings = {}  # Dictionary to store description embeddings with an ID
        self.code_only_embeddings = None
        self.code_desc_embeddings = None
        self.device = "cuda" if torch.cuda.is_available() else "cpu"
        print(f"Using device: {self.device}")

    def load_model(self):
        """Load Google's EmbeddingGemma model"""
        try:
            print("Loading Google's EmbeddingGemma model...")
            self.model = SentenceTransformer(
                "google/embeddinggemma-300m",
                device=self.device
            )
            print("✓ EmbeddingGemma loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading EmbeddingGemma: {e}")
            print("You may need to install the sentence-transformers library: pip install sentence-transformers")
            return False

    def load_data(self):
        """Load function data and create embeddings"""
        try:
            with open('../datas/metta_codebert_complete.json', 'r') as f:
                self.functions = json.load(f)
        except FileNotFoundError:
            print("Error: Run extractor first to create data file")
            return False
        
        print(f"Loaded {len(self.functions)} functions")
        
        # Create embeddings for both strategies
        print("Creating separate embeddings for code and descriptions...")

        # Get lists of texts for embedding
        code_texts = [func['code'] for func in self.functions]
        desc_texts = [func['nl_desc'] for func in self.functions]
        
        # Embed code snippets
        code_vectors = self.embed_texts(code_texts, 'retrieval-document')
        # Embed descriptions
        desc_vectors = self.embed_texts(desc_texts, 'retrieval-document')

        if code_vectors is None or desc_vectors is None:
            return False
        
        # Store embeddings with a unique ID (e.g., func_name or an index)
        # Using a dictionary for easy lookup
        for i, func in enumerate(self.functions):
            # Use a unique identifier, e.g., 'func_name'
            func_id = func['func_name']
            self.code_embeddings[func_id] = code_vectors[i]
            self.desc_embeddings[func_id] = desc_vectors[i]
            
        return True

    def embed_texts(self, texts, task_type):
        """Embed a list of texts using the SentenceTransformer API"""
        if self.model is None:
            return None
        
        try:
            embeddings = self.model.encode(
                texts,
                normalize_embeddings=True,
                convert_to_numpy=True,
                show_progress_bar=True,
                prompt_name=task_type.capitalize()
            )
            return embeddings
        except Exception as e:
            print(f"Error during embedding: {e}")
            return None

    def search_functions(self, query, strategy='desc_only', top_k=5):
        """Search for functions based on user query"""
        if not self.code_embeddings or not self.desc_embeddings:
            print("Please load data first!")
            return None
        
        # Embed the user query
        query_embedding = self.embed_texts([query], 'Retrieval-query')
        if query_embedding is None:
            return None
        
        query_embedding = query_embedding[0] # Take the single vector from the list
        
        results = []
        
        if strategy == 'desc_only':
            # Search using only the description embeddings
            similarities = []
            func_ids = list(self.desc_embeddings.keys())
            for func_id in func_ids:
                desc_vector = self.desc_embeddings[func_id]
                similarity = cosine_similarity(query_embedding.reshape(1, -1), desc_vector.reshape(1, -1))[0][0]
                similarities.append((similarity, func_id))

            similarities.sort(key=lambda x: x[0], reverse=True)
            
            for sim, func_id in similarities[:top_k]:
                # Find the corresponding function details
                func_data = next((f for f in self.functions if f['func_name'] == func_id), None)
                if func_data:
                    results.append({
                        'function': func_data,
                        'similarity': sim,
                        'strategy': 'description_only'
                    })
        else:
            print("Unsupported search strategy.")
            return None
        
        return results

    def display_results(self, results, query):
        """Display search results in a user-friendly way"""
        print(f"\n🔍 Search results for: '{query}'")
        print("=" * 60)
        
        if results:
            print("\n📝 DESCRIPTION-ONLY STRATEGY:")
            print("-" * 40)
            for i, result in enumerate(results, 1):
                func = result['function']
                print(f"{i}. {func['func_name']} (score: {result['similarity']:.3f})")
                if i < len(results):
                    print()
    
    def interactive_search(self):
        """Interactive search loop"""
        print("\n" + "=" * 60)
        print("🔍 INTERACTIVE CODE SEARCH WITH SEPARATE EMBEDDINGS")
        print("=" * 60)
        print("Type what you're looking for and I'll find the best matching functions!")
        print("Type 'quit' to exit.")
        
        while True:
            query = input("\nWhat function are you looking for? ").strip()
            
            if query.lower() == 'quit':
                print("Goodbye! 👋")
                break
            elif query.lower() == '':
                continue
            
            results = self.search_functions(query)
            
            if results:
                self.display_results(results, query)
            else:
                print("Sorry, I couldn't process that search.")

def main():
    """Main interactive search"""
    print("=" * 70)
    print("INTERACTIVE CODE SEARCH")
    print("=" * 70)
    
    search_system = InteractiveGoogleEmbedderRetrieval()
    
    if search_system.load_model() and search_system.load_data():
        search_system.interactive_search()

if __name__ == "__main__":
    main()