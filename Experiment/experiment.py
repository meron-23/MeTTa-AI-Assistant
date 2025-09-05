import numpy as np
from transformers import AutoTokenizer, AutoModel
import torch
import requests
import json

class CodeBERTExperiment:
    def __init__(self):
        self.tokenizer = None
        self.model = None
    
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
    
    def embed_texts(self, texts):
        """Embed a list of texts"""
        if self.model is None:
            print("Model not loaded!")
            return None
        
        try:
            # Tokenize
            inputs = self.tokenizer(
                texts, 
                return_tensors="pt", 
                padding=True, 
                truncation=True, 
                max_length=512
            )
            
            # Generate embeddings
            with torch.no_grad():
                outputs = self.model(**inputs)
            
            # Use [CLS] token embedding
            embeddings = outputs.last_hidden_state[:, 0, :].numpy()
            return embeddings
            
        except Exception as e:
            print(f"Error during embedding: {e}")
            return None
    
    def run_experiment(self):
        """Run the complete experiment"""
        # Load data
        try:
            with open('./data/codebert_code_only.txt', 'r') as f:
                code_only = [line.strip() for line in f if line.strip()]
            
            with open('./data/codebert_code_with_desc.txt', 'r') as f:
                code_with_desc = [line.strip() for line in f if line.strip()]
        except FileNotFoundError:
            print("Error: Run simple_codebert_embedder.py first")
            return
        
        print(f"Code-only samples: {len(code_only)}")
        print(f"Code+description samples: {len(code_with_desc)}")
        
        # Use smaller subset for testing
        sample_size = min(10, len(code_only))
        code_only = code_only[:sample_size]
        code_with_desc = code_with_desc[:sample_size]
        
        print(f"\nUsing {sample_size} samples for experiment...")
        
        # Embed code-only
        print("\n1. Embedding code-only...")
        code_embeddings = self.embed_texts(code_only)
        if code_embeddings is not None:
            np.save('./data/experiment_code_only.npy', code_embeddings)
            print(f"✓ Code-only embeddings shape: {code_embeddings.shape}")
        
        # Embed code + description
        print("\n2. Embedding code + description...")
        combined_embeddings = self.embed_texts(code_with_desc)
        if combined_embeddings is not None:
            np.save('./data/experiment_combined.npy', combined_embeddings)
            print(f"✓ Combined embeddings shape: {combined_embeddings.shape}")
        
        # Compare results
        if code_embeddings is not None and combined_embeddings is not None:
            self.compare_embeddings(code_embeddings, combined_embeddings)
    
    def compare_embeddings(self, code_embeds, combined_embeds):
        """Compare the two embedding approaches"""
        from sklearn.metrics.pairwise import cosine_similarity
        
        similarities = []
        for i in range(min(len(code_embeds), len(combined_embeds))):
            sim = cosine_similarity(
                code_embeds[i].reshape(1, -1), 
                combined_embeds[i].reshape(1, -1)
            )[0][0]
            similarities.append(sim)
        
        print(f"\n=== RESULTS ===")
        print(f"Average similarity: {np.mean(similarities):.4f}")
        print(f"Min similarity: {np.min(similarities):.4f}")
        print(f"Max similarity: {np.max(similarities):.4f}")
        print(f"Std deviation: {np.std(similarities):.4f}")

def main():
    """Main experiment"""
    print("=" * 50)
    print("CODEBERT META CODE EXPERIMENT")
    print("=" * 50)
    
    experiment = CodeBERTExperiment()
    
    if experiment.load_model():
        experiment.run_experiment()

if __name__ == "__main__":
    main()