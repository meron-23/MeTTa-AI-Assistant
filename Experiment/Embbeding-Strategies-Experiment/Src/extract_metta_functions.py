import re
import json

def extract_metta_functions(metta_code_string):
    """
    Extracts function documentation and code from a MeTTa code string.
    """
    functions = []
    
    # Split the code into blocks based on the "Public MeTTa" comment
    # The regex pattern splits at "Public MeTTa" and captures everything that follows
    function_blocks = re.split(r';;\s*Public MeTTa', metta_code_string)[1:]

    for block in function_blocks:
        if not block.strip():
            continue

        func_data = {}
        
        # Regex to capture the function's name and documentation
        doc_match = re.search(r'@doc\s+(\w+)', block)
        if doc_match:
            func_data['func_name'] = doc_match.group(1).strip()
        else:
            continue

        # Regex to capture the description
        desc_match = re.search(r'@desc\s+"(.*?)"', block, re.DOTALL)
        if desc_match:
            func_data['desc'] = desc_match.group(1).strip()

        # Regex to capture the return value
        return_match = re.search(r'@return\s+"(.*?)"', block, re.DOTALL)
        if return_match:
            func_data['return'] = return_match.group(1).strip()
            
        # Regex to capture the parameters, including multiple
        params_matches = re.findall(r'@param\s+"(.*?)"', block, re.DOTALL)
        if params_matches:
            func_data['params'] = params_matches

        # Regex to capture the type signature and implementation code
        code_match = re.search(r'(:.*?;; Implemented.*?)', block, re.DOTALL)
        if code_match:
            full_code = code_match.group(1).strip()
            func_data['code'] = full_code
            
            # Combine code and description for the Code+Description strategy
            if 'desc' in func_data:
                func_data['code_with_desc'] = func_data['desc'] + " " + full_code
            else:
                func_data['code_with_desc'] = full_code

        functions.append(func_data)
        
    return functions

def main():
    """Main function to run the extraction and save to a JSON file."""
    try:
        with open('./Data/chatgpt_knowledge_doc.txt', 'r', encoding='utf-8') as f:
            metta_code = f.read()
    except FileNotFoundError:
        print("Error: 'metta_code.txt' not found. Please create this file with your MeTTa code.")
        return

    extracted_functions = extract_metta_functions(metta_code)

    if extracted_functions:
        with open('datas/metta_data.json', 'w') as f:
            json.dump(extracted_functions, f, indent=4)
        print(f"✓ Successfully extracted {len(extracted_functions)} functions and saved to datas/test_data.json")
    else:
        print("No functions were extracted. Please check the input code format.")

if __name__ == "__main__":
    main()