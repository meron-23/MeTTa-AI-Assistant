import re
import json
from typing import List, Dict, Any

def extract_functions_for_codebert(content: str) -> List[Dict[str, str]]:
    """
    Extract functions with both code and natural language descriptions for CodeBERT.
    """
    functions = []
    
    # Remove comments for cleaner parsing
    cleaned_content = re.sub(r';.*$', '', content, flags=re.MULTILINE)
    
    # Find all function documentation blocks
    doc_pattern = r'\(@doc\s+(\w+)(.*?)\)\)'
    doc_matches = re.finditer(doc_pattern, cleaned_content, re.DOTALL)
    
    for doc_match in doc_matches:
        func_name = doc_match.group(1)
        doc_content = doc_match.group(2)
        
        # Extract natural language description
        natural_language_desc = extract_natural_language(doc_content)
        
        # Find the corresponding code implementation
        code_implementation = find_function_implementation(cleaned_content, func_name, doc_match.end())
        
        if code_implementation:
            # Clean the code for better embedding
            clean_code = clean_code_for_embedding(code_implementation)
            
            functions.append({
                "code": clean_code,
                "nl_desc": natural_language_desc,
                "func_name": func_name,
                "code_with_desc": f"{natural_language_desc} [SEP] {clean_code}"  # For combined embedding
            })
    
    return functions

def extract_natural_language(doc_content: str) -> str:
    """
    Extract natural language descriptions from documentation.
    """
    nl_parts = []
    
    # Extract @desc content
    desc_match = re.search(r'\(@desc\s+"([^"]+)"\)', doc_content)
    if desc_match:
        nl_parts.append(desc_match.group(1))
    
    # Extract @param descriptions
    param_matches = re.findall(r'\(@param\s+"([^"]+)"\)', doc_content)
    if param_matches:
        nl_parts.append("Parameters: " + "; ".join(param_matches))
    
    # Extract @return description
    return_match = re.search(r'\(@return\s+"([^"]+)"\)', doc_content)
    if return_match:
        nl_parts.append("Returns: " + return_match.group(1))
    
    return " | ".join(nl_parts)

def find_function_implementation(content: str, func_name: str, start_pos: int) -> str:
    """
    Find the complete function implementation.
    """
    remaining_content = content[start_pos:]
    code_parts = []
    
    # Look for type signature
    type_pattern = rf'\(:\s+{re.escape(func_name)}\s+\(->[^)]+\)\)'
    type_match = re.search(type_pattern, remaining_content)
    if type_match:
        code_parts.append(type_match.group(0))
    
    # Look for implementations
    impl_pattern = rf'(\(=\s+\({re.escape(func_name)}[^)]+\)[^)]+\)|\(ALT=\s+\({re.escape(func_name)}[^)]+\)[^)]+\))'
    impl_matches = re.finditer(impl_pattern, remaining_content, re.DOTALL)
    
    for impl_match in impl_matches:
        code_parts.append(impl_match.group(0))
    
    return "\n".join(code_parts) if code_parts else None

def clean_code_for_embedding(code: str) -> str:
    """
    Clean the code for better embedding performance.
    """
    # Remove excessive whitespace but keep structure
    code = re.sub(r'\s+', ' ', code)
    # Normalize parentheses
    code = re.sub(r'\(\s+', '(', code)
    code = re.sub(r'\s+\)', ')', code)
    # Remove trailing/leading spaces
    code = code.strip()
    return code

def save_for_codebert_embedding(functions: List[Dict[str, str]], output_base: str):
    """
    Save functions in formats for both embedding scenarios.
    """
    # 1. CODE-ONLY EMBEDDING
    with open(f"{output_base}_code_only.txt", 'w', encoding='utf-8') as f:
        for func in functions:
            f.write(func["code"] + '\n')
    
    # 2. CODE + DESCRIPTION EMBEDDING (using [SEP] token)
    with open(f"{output_base}_code_with_desc.txt", 'w', encoding='utf-8') as f:
        for func in functions:
            f.write(func["code_with_desc"] + '\n')
    
    # 3. Separate files for flexibility
    with open(f"{output_base}_descriptions_only.txt", 'w', encoding='utf-8') as f:
        for func in functions:
            f.write(func["nl_desc"] + '\n')
    
    # 4. JSON with all information
    with open(f"{output_base}_complete.json", 'w', encoding='utf-8') as f:
        json.dump(functions, f, indent=2, ensure_ascii=False)
    
    print(f"Saved {len(functions)} functions for CodeBERT embedding")
    print(f"Files created:")
    print(f"  - {output_base}_code_only.txt (for code-only embedding)")
    print(f"  - {output_base}_code_with_desc.txt (for code+description embedding)")
    print(f"  - {output_base}_descriptions_only.txt (descriptions only)")
    print(f"  - {output_base}_complete.json (complete dataset)")

def main():
    input_file = "./data/chatgpt_knowledge_doc.txt"
    output_base = "./data/metta_codebert"
    
    try:
        print("Extracting MeTTa functions for CodeBERT...")
        with open(input_file, 'r', encoding='utf-8') as f:
            content = f.read()
        
        functions = extract_functions_for_codebert(content)
        print(f"Found {len(functions)} functions")
        
        # Save data for both embedding scenarios
        save_for_codebert_embedding(functions, output_base)
        
        # Show examples
        if functions:
            print("\n=== Sample Output ===")
            print("\n1. CODE-ONLY example:")
            print(functions[0]["code"][:100] + "...")
            
            print("\n2. CODE + DESCRIPTION example:")
            print(functions[0]["code_with_desc"][:150] + "...")
        
    except Exception as e:
        print(f"Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()