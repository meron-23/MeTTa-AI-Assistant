import numpy as np
import torch
import json
from sklearn.metrics.pairwise import cosine_similarity
from sentence_transformers import SentenceTransformer

class InteractiveGoogleEmbedderRetrieval:
    def __init__(self):
        self.model = None
        self.functions = None
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
            # EmbeddingGemma is already optimized for this, no need for separate tokenizer/model
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
        print("Creating embeddings...")
        
        # Strategy 1: Code-only
        code_only_texts = [func['code'] for func in self.functions]
        # Use task_type='retrieval_document' for the code snippets
        self.code_only_embeddings = self.embed_texts(code_only_texts, 'retrieval-document')
        
        # Strategy 2: Code+description
        code_desc_texts = [func['code_with_desc'] for func in self.functions]
        # Use task_type='retrieval_document' for the code snippets with descriptions
        self.code_desc_embeddings = self.embed_texts(code_desc_texts, 'retrieval-document')
        
        return self.code_only_embeddings is not None and self.code_desc_embeddings is not None

    def embed_texts(self, texts, task_type):
        """Embed a list of texts using the SentenceTransformer API"""
        if self.model is None:
            return None
        
        try:
            # The SentenceTransformer model automatically handles tokenization,
            # batching, and pooling, and can be given a task type.
            # Using normalize_embeddings=True is crucial for cosine similarity.
            embeddings = self.model.encode(
                texts,
                normalize_embeddings=True,
                convert_to_numpy=True,
                show_progress_bar=True,
                # EmbeddingGemma uses prompts to guide its embedding
                prompt_name=task_type.capitalize() 
            )
            return embeddings
            
        except Exception as e:
            print(f"Error during embedding: {e}")
            return None

    def search_functions(self, query, strategy='both', top_k=5):
        """Search for functions based on user query"""
        if self.functions is None or self.code_only_embeddings is None:
            print("Please load data first!")
            return None
        
        # Embed the user query using the "retrieval_query" task type
        query_embedding = self.embed_texts([query], 'Retrieval-query')
        if query_embedding is None:
            return None
        
        results = {}
        
        if strategy in ['both', 'code_only']:
            # Search in code-only database
            similarities = cosine_similarity(query_embedding, self.code_only_embeddings)[0]
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            code_only_results = []
            for idx in top_indices:
                code_only_results.append({
                    'function': self.functions[idx],
                    'similarity': similarities[idx],
                    'strategy': 'code_only'
                })
            results['code_only'] = code_only_results
        
        if strategy in ['both', 'code_desc']:
            # Search in code+description database
            similarities = cosine_similarity(query_embedding, self.code_desc_embeddings)[0]
            top_indices = np.argsort(similarities)[::-1][:top_k]
            
            code_desc_results = []
            for idx in top_indices:
                code_desc_results.append({
                    'function': self.functions[idx],
                    'similarity': similarities[idx],
                    'strategy': 'code_desc'
                })
            results['code_desc'] = code_desc_results
        
        return results

    def display_results(self, results, query):
        """Display search results in a user-friendly way"""
        print(f"\n🔍 Search results for: '{query}'")
        print("=" * 60)
        
        if 'code_only' in results:
            print("\n📋 CODE-ONLY STRATEGY:")
            print("-" * 40)
            for i, result in enumerate(results['code_only'], 1):
                func = result['function']
                print(f"{i}. {func['func_name']} (score: {result['similarity']:.3f})")
                #print(f"Code: {func['code'][:80].replace('\\n', ' ')}...")
                if i < len(results['code_only']):
                    print()
        
        if 'code_desc' in results:
            print("\n📝 CODE+DESCRIPTION STRATEGY:")
            print("-" * 40)
            for i, result in enumerate(results['code_desc'], 1):
                func = result['function']
                print(f"{i}. {func['func_name']} (score: {result['similarity']:.3f})")
                #print(f"Code: {func['code'][:80].replace('\\n', ' ')}...")
                if i < len(results['code_desc']):
                    print()
        
        # Compare strategies if both are present
        if 'code_only' in results and 'code_desc' in results:
            self.compare_strategies(results)
    
    def compare_strategies(self, results):
        """Compare the two strategies"""
        print("\n⚖️  STRATEGY COMPARISON:")
        print("-" * 30)
        
        co_top = results['code_only'][0]
        cd_top = results['code_desc'][0]
        
        print(f"Code-only top result:  {co_top['function']['func_name']} ({co_top['similarity']:.3f})")
        print(f"Code+desc top result:  {cd_top['function']['func_name']} ({cd_top['similarity']:.3f})")
        
        if co_top['function']['func_name'] == cd_top['function']['func_name']:
            print("✅ Both strategies agree on the top result!")
        else:
            print("❌ Strategies disagree on the top result")
            
        # Show which strategy has higher confidence
        if co_top['similarity'] > cd_top['similarity']:
            print("📈 Code-only has higher confidence")
        else:
            print("📈 Code+description has higher confidence")
            
    def interactive_search(self):
        """Interactive search loop"""
        print("\n" + "=" * 60)
        print("🔍 INTERACTIVE CODE SEARCH WITH GOOGLE'S EMBEDDINGGEMMA")
        print("=" * 60)
        print("Type what you're looking for and I'll find the best matching functions!")
        print("Type 'quit' to exit.")
        
        # The change_strategy logic is simplified to always use both for comparison.
        # You can re-implement it if you need different modes.
        current_strategy = 'both'
        
        while True:
            query = input("\nWhat function are you looking for? ").strip()
            
            if query.lower() == 'quit':
                print("Goodbye! 👋")
                break
            elif query.lower() == '':
                continue
            
            # Perform search
            results = self.search_functions(query, strategy=current_strategy)
            
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