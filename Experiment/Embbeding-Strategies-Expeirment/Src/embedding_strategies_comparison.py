import numpy as np
import torch
import json
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class InteractiveGoogleEmbedderRetrieval:
    def __init__(self):
        self.model = None
        self.functions = None
        # Approach 1: Code only
        self.code_only_embeddings = None
        # Approach 2: Code with description combined
        self.code_desc_embeddings_combined = None
        # Approach 3: Separate embeddings
        self.code_embeddings_separate = {}
        self.desc_embeddings_separate = {}
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
        """Load function data and create embeddings for all three approaches"""
        try:
            with open('../datas/metta_codebert_complete.json', 'r') as f:
                self.functions = json.load(f)
        except FileNotFoundError:
            print("Error: Run extractor first to create data file")
            return False
        
        print(f"Loaded {len(self.functions)} functions")
        
        print("Creating embeddings for all three approaches...")
        
        # --- Approach 1: Code-only ---
        code_only_texts = [func['code'] for func in self.functions]
        # Use task_type='retrieval_document' for the code snippets
        self.code_only_embeddings = self.embed_texts(code_only_texts, 'retrieval-document')
        
        # --- Approach 2: Code+description combined ---
        code_desc_combined_texts = [func['code_with_desc'] for func in self.functions]
        self.code_desc_embeddings_combined = self.embed_texts(code_desc_combined_texts, 'retrieval-document')
        
        # --- Approach 3: Separate embeddings ---
        code_texts_separate = [func['code'] for func in self.functions]
        desc_texts_separate = [func['nl_desc'] for func in self.functions]
        
        code_vectors = self.embed_texts(code_texts_separate, 'retrieval-document')
        desc_vectors = self.embed_texts(desc_texts_separate, 'retrieval-document')
        
        if code_vectors is None or desc_vectors is None:
            return False
        
        for i, func in enumerate(self.functions):
            func_id = func['func_name']
            self.code_embeddings_separate[func_id] = code_vectors[i]
            self.desc_embeddings_separate[func_id] = desc_vectors[i]
            
        return (self.code_only_embeddings is not None and
                self.code_desc_embeddings_combined is not None and
                self.code_embeddings_separate is not None)

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
    
    def search_functions(self, query, top_k=5):
        """
        Search for functions based on a query using all three approaches.
        Returns a dictionary of results for each approach.
        """
        if not all([self.code_only_embeddings is not None, 
                    self.code_desc_embeddings_combined is not None,
                    self.code_embeddings_separate is not None]):
            print("Please load data first!")
            return None
        
        query_embedding = self.embed_texts([query], 'Retrieval-query')
        if query_embedding is None:
            return None
        query_embedding = query_embedding[0].reshape(1, -1)
        
        results = {}

        # --- Approach 1: Code-only search ---
        similarities = cosine_similarity(query_embedding, self.code_only_embeddings)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        code_only_results = [{
            'function': self.functions[idx],
            'similarity': similarities[idx],
            'strategy': 'code_only'
        } for idx in top_indices]
        results['code_only'] = code_only_results

        # --- Approach 2: Code+Description combined search ---
        similarities = cosine_similarity(query_embedding, self.code_desc_embeddings_combined)[0]
        top_indices = np.argsort(similarities)[::-1][:top_k]
        code_desc_combined_results = [{
            'function': self.functions[idx],
            'similarity': similarities[idx],
            'strategy': 'code_desc_combined'
        } for idx in top_indices]
        results['code_desc_combined'] = code_desc_combined_results
        
        # --- Approach 3: Separate embeddings search (Example: weighted sum) ---
        # This approach requires a decision on how to combine code and description similarity scores.
        # A simple method is to average them.
        separate_results = []
        func_ids = list(self.code_embeddings_separate.keys())
        all_scores = []
        for func_id in func_ids:
            code_vector = self.code_embeddings_separate[func_id].reshape(1, -1)
            desc_vector = self.desc_embeddings_separate[func_id].reshape(1, -1)
            
            # Calculate similarities
            code_sim = cosine_similarity(query_embedding, code_vector)[0][0]
            desc_sim = cosine_similarity(query_embedding, desc_vector)[0][0]
            
            # Simple average of scores
            combined_sim = (code_sim + desc_sim) / 2
            
            all_scores.append((combined_sim, func_id, code_sim, desc_sim))

        all_scores.sort(key=lambda x: x[0], reverse=True)
        
        for score, func_id, code_sim, desc_sim in all_scores[:top_k]:
            func_data = next((f for f in self.functions if f['func_name'] == func_id), None)
            if func_data:
                separate_results.append({
                    'function': func_data,
                    'similarity': score,
                    'strategy': 'separate_embeddings',
                    'code_sim': code_sim,
                    'desc_sim': desc_sim
                })
        results['separate_embeddings'] = separate_results
        
        return results

    def display_results(self, results, query):
        """Display search results for all three approaches"""
        print(f"\n🔍 Search results for: '{query}'")
        print("=" * 60)
        
        # Displaying results for Approach 1: Code-only
        print("\n📋 APPROACH 1: CODE-ONLY STRATEGY:")
        print("-" * 40)
        for i, res in enumerate(results['code_only'], 1):
            print(f"{i}. {res['function']['func_name']} (score: {res['similarity']:.3f})")

        # Displaying results for Approach 2: Code+Description combined
        print("\n📝 APPROACH 2: CODE+DESCRIPTION (COMBINED) STRATEGY:")
        print("-" * 40)
        for i, res in enumerate(results['code_desc_combined'], 1):
            print(f"{i}. {res['function']['func_name']} (score: {res['similarity']:.3f})")

        # Displaying results for Approach 3: Separate Embeddings
        print("\n✨ APPROACH 3: CODE+DESCRIPTION (SEPARATE) STRATEGY:")
        print("-" * 40)
        for i, res in enumerate(results['separate_embeddings'], 1):
            print(f"{i}. {res['function']['func_name']} (score: {res['similarity']:.3f}, code_sim: {res['code_sim']:.3f}, desc_sim: {res['desc_sim']:.3f})")
        
        # Additional comparison
        print("\n📊 COMPARISON OF TOP RESULTS:")
        print("-" * 30)
        co_top = results['code_only'][0]
        cd_top = results['code_desc_combined'][0]
        se_top = results['separate_embeddings'][0]

        print(f"Top Result (Code-only):         {co_top['function']['func_name']} ({co_top['similarity']:.3f})")
        print(f"Top Result (Combined):          {cd_top['function']['func_name']} ({cd_top['similarity']:.3f})")
        print(f"Top Result (Separate/Weighted): {se_top['function']['func_name']} ({se_top['similarity']:.3f})")

    def interactive_search(self):
        """Interactive search loop"""
        print("\n" + "=" * 60)
        print("🔍 INTERACTIVE CODE SEARCH - ALL 3 APPROACHES")
        print("=" * 60)
        print("Type a query to compare the results of different embedding strategies.")
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