import metta_parser 
import argparse
from typing import List

# Recursive Chunking Algorithm (with source_code passed as an argument)

def GETSIZE(node: metta_parser.SyntaxNode) -> int:
    """Gets the size of a node based on its source text length."""
    start, end = node.src_range
    return end - start

def CHUNKNODES(nodes: List[metta_parser.SyntaxNode], source_code: str, max_size: int) -> List[str]:
    """Chunks a list of sibling nodes."""
    chunks = []
    current_chunk_nodes, current_size = [], 0
    
    for node in nodes:
        node_size = GETSIZE(node)
        
        # Condition where adding to the current chunk would exceed max_size
        if current_chunk_nodes and (current_size + node_size) > max_size:
            # Combine node texts to form the chunk content
            start_char = current_chunk_nodes[0].src_range[0]
            end_char = current_chunk_nodes[-1].src_range[1]
            chunks.append(source_code[start_char:end_char])
            current_chunk_nodes, current_size = [], 0

        # If the node itself is too large, recursively chunk its children
        if node_size > max_size:
            if current_chunk_nodes:
                start_char = current_chunk_nodes[0].src_range[0]
                end_char = current_chunk_nodes[-1].src_range[1]
                chunks.append(source_code[start_char:end_char])
                current_chunk_nodes, current_size = [], 0

            subchunks = CHUNKNODES(node.sub_nodes, source_code, max_size)
            chunks.extend(subchunks)
        # If the node fits, add it to the current chunk
        else:
            current_chunk_nodes.append(node)
            current_size += node_size
            
    # Add the last remaining chunk if it exists
    if current_chunk_nodes:
        start_char = current_chunk_nodes[0].src_range[0]
        end_char = current_chunk_nodes[-1].src_range[1]
        chunks.append(source_code[start_char:end_char])
        
    return chunks

def CHUNKCODE(code: str, max_size: int) -> List[str]:
    """Entry point for the chunking algorithm."""
    # If the entire code is small enough, return it as a single chunk
    if len(code) <= max_size:
        return [code]
    
    try:
        # The top-level nodes are the children of the whole "file"
        tree_children = metta_parser.parse(code)
        return CHUNKNODES(tree_children, code, max_size)
    except ValueError as e:
        print(f"Error parsing MeTTa code: {e}")
        return []


def main():
    parser = argparse.ArgumentParser(description="Chunk a MeTTa source file using an AST-based algorithm.")
    parser.add_argument("input_file", help="Path to the input .metta file to be chunked.")
    parser.add_argument("output_file", help="Path to the output file where chunks will be written.")
    parser.add_argument("--max-size", type=int, default=500, help="The maximum character size for each chunk (default: 500).")
    
    args = parser.parse_args()

    print(f"Reading from '{args.input_file}'...")
    try:
        with open(args.input_file, 'r', encoding='utf-8') as f:
            source_code = f.read()
            print(source_code[:1000])
    except FileNotFoundError:
        print(f"Error: Input file not found at '{args.input_file}'")
        return

    print(f"Chunking code with MAX_SIZE = {args.max_size}...")
    final_chunks = CHUNKCODE(source_code, args.max_size)
    
    print(f"Generated {len(final_chunks)} chunks. Writing to '{args.output_file}'...")
    try:
        with open(args.output_file, 'w', encoding='utf-8') as f:
            for i, chunk in enumerate(final_chunks):
                f.write(f"--- CHUNK {i+1} (Size: {len(chunk)}) ---\n\n")
                f.write(chunk.strip() + "\n\n")
    except IOError as e:
        print(f"Error writing to file '{args.output_file}': {e}")
        return

    print("Chunking complete!")

if __name__ == "__main__":
    main()
