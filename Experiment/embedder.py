import numpy as np
import json

def load_data():
    """Load the extracted functions"""
    try:
        with open('./data/metta_codebert_complete.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        print("Error: Run metta_extractor.py first to create the data file")
        return []

def prepare_embeddings_data(functions):
    """Prepare data for both embedding scenarios"""
    code_only = []
    code_with_desc = []
    
    for func in functions:
        code_only.append(func['code'])
        code_with_desc.append(func['code_with_desc'])
    
    return code_only, code_with_desc

def save_embedding_data(code_only, code_with_desc):
    """Save the data for embedding"""
    # Save code-only
    with open('./data/codebert_code_only.txt', 'w', encoding='utf-8') as f:
        for code in code_only:
            f.write(code + '\n')
    
    # Save code + description
    with open('codebert_code_with_desc.txt', 'w', encoding='utf-8') as f:
        for code_desc in code_with_desc:
            f.write(code_desc + '\n')
    
    print(f"Saved {len(code_only)} code samples")
    print(f"Saved {len(code_with_desc)} code+description samples")

def main():
    """Main function"""
    print("=" * 50)
    print("SIMPLE CODEBERT DATA PREPARATION")
    print("=" * 50)
    
    # Load the extracted functions
    functions = load_data()
    if not functions:
        return
    
    print(f"Loaded {len(functions)} functions")
    
    # Prepare data for both experiments
    code_only, code_with_desc = prepare_embeddings_data(functions)
    
    # Save the data files
    save_embedding_data(code_only, code_with_desc)
    
    print("\nData ready for CodeBERT embedding!")
    print("\nNext steps:")
    print("1. Use codebert_code_only.txt for code-only embedding")
    print("2. Use codebert_code_with_desc.txt for code+description embedding")
    print("3. Compare the results to see which works better")

if __name__ == "__main__":
    main()