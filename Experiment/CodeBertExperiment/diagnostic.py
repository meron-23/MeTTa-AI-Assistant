import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import json
from sklearn.metrics.pairwise import cosine_similarity
import matplotlib.pyplot as plt

class DiagnosticRetrieval:
    def __init__(self):
        self.tokenizer = None
        self.model = None
        self.functions = None
        self.embeddings = None
    
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
        """Load function data"""
        try:
            with open('datas/python_test_data.json', 'r') as f:
                self.functions = json.load(f)
            print(f"Loaded {len(self.functions)} functions")
            return True
        except FileNotFoundError:
            print("Error: Run extractor first")
            return False
    
    def analyze_embeddings(self):
        """Analyze why retrieval isn't working"""
        # Create embeddings for all functions
        all_texts = [f"{func['func_name']}: {func['code']}" for func in self.functions]
        self.embeddings = self.embed_texts(all_texts)
        
        if self.embeddings is None:
            return
        
        print("\n🔍 DIAGNOSTIC ANALYSIS")
        print("=" * 50)
        
        # 1. Check embedding similarity distribution
        self.check_similarity_distribution()
        
        # 2. Check if embeddings are diverse enough
        self.check_embedding_diversity()
        
        # 3. Test with specific queries
        self.test_problematic_queries()
    
    def check_similarity_distribution(self):
        """Check if all embeddings are too similar"""
        print("\n1. SIMILARITY DISTRIBUTION:")
        
        # Calculate pairwise similarities
        similarities = cosine_similarity(self.embeddings)
        np.fill_diagonal(similarities, 0)  # Remove self-similarity
        
        avg_similarity = np.mean(similarities)
        min_similarity = np.min(similarities)
        max_similarity = np.max(similarities)
        
        print(f"Average similarity between functions: {avg_similarity:.4f}")
        print(f"Minimum similarity: {min_similarity:.4f}")
        print(f"Maximum similarity: {max_similarity:.4f}")
        
        if avg_similarity > 0.9:
            print("❌ PROBLEM: Embeddings are too similar! Everything looks the same to CodeBERT.")
        else:
            print("✓ Embeddings have good diversity")
    
    def check_embedding_diversity(self):
        """Check if embeddings capture meaningful differences"""
        print("\n2. EMBEDDING DIVERSITY:")
        
        # Calculate variance in embedding space
        embedding_variance = np.var(self.embeddings, axis=0)
        avg_variance = np.mean(embedding_variance)
        
        print(f"Average variance across dimensions: {avg_variance:.6f}")
        
        if avg_variance < 0.01:
            print("❌ PROBLEM: Embeddings have low variance - not capturing differences well")
        else:
            print("✓ Embeddings have reasonable variance")
    
    def test_problematic_queries(self):
        """Test why queries aren't working"""
        print("\n3. QUERY ANALYSIS:")
        
        test_queries = [
            "addition function",
            "error handling", 
            "list operations",
            "type conversion"
        ]
        
        query_embeddings = self.embed_texts(test_queries)
        
        for i, query in enumerate(test_queries):
            similarities = cosine_similarity([query_embeddings[i]], self.embeddings)[0]
            top_5_indices = np.argsort(similarities)[::-1][:5]
            top_5_similarities = similarities[top_5_indices]
            top_5_funcs = [self.functions[idx]['func_name'] for idx in top_5_indices]
            
            print(f"\nQuery: '{query}'")
            print(f"Top 5 matches: {top_5_funcs}")
            print(f"Similarities: {top_5_similarities.round(3)}")
            
            # Check if results make sense
            if self.are_results_relevant(query, top_5_funcs):
                print("✓ Results seem relevant")
            else:
                print("❌ Results don't make sense!")
    
    def are_results_relevant(self, query, results):
        """Check if results are relevant to query"""
        query = query.lower()
        
        # Simple relevance checks
        if 'add' in query and any('+' in func or 'add' in func.lower() for func in results):
            return True
        if 'error' in query and any('error' in func.lower() for func in results):
            return True
        if 'list' in query and any('map' in func.lower() or 'filter' in func.lower() for func in results):
            return True
        
        return False
    
    def embed_texts(self, texts):
        """Embed texts with CodeBERT"""
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
            
            return outputs.last_hidden_state[:, 0, :].numpy()
            
        except Exception as e:
            print(f"Embedding error: {e}")
            return None
    
    def suggest_fixes(self):
        """Suggest fixes for the retrieval problem"""
        print("\n💡 SUGGESTED FIXES:")
        print("=" * 50)
        
        print("1. 🎯 TRY DIFFERENT POOLING STRATEGY:")
        print("   - Instead of [CLS] token, try mean pooling")
        print("   - Or try using the last hidden state differently")
        
        print("\n2. 🔧 FINE-TUNE CODEBERT ON METTA:")
        print("   - CodeBERT was trained on Python/Java/etc.")
        print("   - It may not understand MeTTa syntax well")
        print("   - Fine-tuning on MeTTa code would help")
        
        print("\n3. 📝 BETTER QUERY PROCESSING:")
        print("   - Preprocess queries to match MeTTa terminology")
        print("   - Use synonym expansion for MeTTa concepts")
        
        print("\n4. 🏗️  USE DIFFERENT EMBEDDING APPROACH:")
        print("   - Try sentence-transformers instead of raw CodeBERT")
        print("   - Or use OpenAI embeddings as a baseline")

def main():
    """Run diagnostic analysis"""
    print("=" * 70)
    print("DIAGNOSTIC ANALYSIS: WHY RETRIEVAL ISN'T WORKING")
    print("=" * 70)
    
    diagnostic = DiagnosticRetrieval()
    
    if diagnostic.load_model() and diagnostic.load_data():
        diagnostic.analyze_embeddings()
        diagnostic.suggest_fixes()

if __name__ == "__main__":
    main()