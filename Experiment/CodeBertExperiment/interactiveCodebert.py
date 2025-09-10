import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import json
from sklearn.metrics.pairwise import cosine_similarity

class InteractiveCodeBERTRetrieval:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.functions = None
        self.code_only_embeddings = None
        self.code_desc_embeddings = None
    
    def load_model(self):
        """Load CodeBERT model"""
        try:
            print("Loading CodeBERT model...")
            self.tokenizer = AutoTokenizer.from_pretrained("microsoft/codebert-base")
            self.model = AutoModel.from_pretrained("microsoft/codebert-base")
            print("✓ CodeBERT loaded successfully!")
            return True
        except Exception as e:
            print(f"Error loading CodeBERT: {e}")
            return False
    
    def load_data(self):
        """Load function data and create embeddings"""
        try:
            with open('datas/python_test_data.json', 'r') as f:
                self.functions = json.load(f)
        except FileNotFoundError:
            print("Error: Run extractor first to create data file")
            return False
        
        print(f"Loaded {len(self.functions)} functions")
        
        # Create embeddings for both strategies
        print("Creating embeddings...")
        
        # Strategy 1: Code-only
        code_only_texts = [func['code'] for func in self.functions]
        self.code_only_embeddings = self.embed_texts(code_only_texts)
        
        # Strategy 2: Code+description
        code_desc_texts = [func['code_with_desc'] for func in self.functions]
        self.code_desc_embeddings = self.embed_texts(code_desc_texts)
        
        return self.code_only_embeddings is not None and self.code_desc_embeddings is not None
    
    def embed_texts(self, texts):
        """Embed a list of texts"""
        if self.model is None:
            return None
        
        try:
            inputs = self.tokenizer(
                texts, 
                return_tensors="pt", 
                padding=True, 
                truncation=True, 
                max_length=512
            )
            
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Use [CLS] token embedding
            embeddings = outputs.last_hidden_state[:, 0, :].numpy()
            return embeddings
            
        except Exception as e:
            print(f"Error during embedding: {e}")
            return None
    
    def search_functions(self, query, strategy='both', top_k=5):
        """Search for functions based on user query"""
        if self.functions is None or self.code_only_embeddings is None:
            print("Please load data first!")
            return None
        
        # Embed the user query
        query_embedding = self.embed_texts([query])
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
                print(f"   Code: {func['code'][:80]}...")
                if i < len(results['code_only']):
                    print()
        
        if 'code_desc' in results:
            print("\n📝 CODE+DESCRIPTION STRATEGY:")
            print("-" * 40)
            for i, result in enumerate(results['code_desc'], 1):
                func = result['function']
                print(f"{i}. {func['func_name']} (score: {result['similarity']:.3f})")
                print(f"   Code: {func['code'][:80]}...")
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
        print("🔍 INTERACTIVE CODEBERT SEARCH")
        print("=" * 60)
        print("Type what you're looking for and I'll find the best matching MeTTa functions!")
        print("Type 'quit' to exit, 'strategies' to change search mode")
        
        current_strategy = 'both'  # Default: show both strategies
        
        while True:
            print(f"\nCurrent search mode: {current_strategy}")
            query = input("\nWhat function are you looking for? ").strip()
            
            if query.lower() == 'quit':
                print("Goodbye! 👋")
                break
            elif query.lower() == 'strategies':
                self.change_strategy()
                continue
            elif query.lower() == '':
                continue
            
            # Perform search
            results = self.search_functions(query, strategy=current_strategy)
            
            if results:
                self.display_results(results, query)
            else:
                print("Sorry, I couldn't process that search.")
    
    def change_strategy(self):
        """Let user change search strategy"""
        print("\nAvailable search strategies:")
        print("1. Both strategies (code-only and code+description)")
        print("2. Code-only only")
        print("3. Code+description only")
        
        choice = input("Choose strategy (1-3): ").strip()
        
        if choice == '1':
            return 'both'
        elif choice == '2':
            return 'code_only'
        elif choice == '3':
            return 'code_desc'
        else:
            print("Invalid choice, keeping current strategy")
            return 'both'

def main():
    """Main interactive search"""
    print("=" * 70)
    print("INTERACTIVE CODEBERT FUNCTION SEARCH")
    print("=" * 70)
    
    search_system = InteractiveCodeBERTRetrieval()
    
    if search_system.load_model() and search_system.load_data():
        search_system.interactive_search()

if __name__ == "__main__":
    main()
    #try embedding python and test