import os
import argparse
import psycopg
import metta_ast_parser 
from typing import List
from db import Database as DB
from dotenv import load_dotenv
from preprocess import preprocess_code

# Recursive Chunking Algorithm (with source_code passed as an argument)

def getSize(node: metta_ast_parser.SyntaxNode) -> int:
    """Gets the size of a node based on its source text length."""
    start, end = node.src_range
    return end - start

def ChunkPreprocessedCode(potential_chunks, max_size: int, db: DB, source_code: str) -> List[str]:
    """Chunks a list of potential chunks based on max_size.
    Each potential chunk is a list of text_node table IDs from our db.
    Returns a list of chunked code strings.
    """
    chunks = []

    for chunk_ids in potential_chunks:
        chunk, chunk_size = [], 0
        for chunk_id in chunk_ids:
            text_range = db.get_text_node(chunk_id)[1]
            text_node = source_code[text_range[0]:text_range[1]]
            text_size = len(text_node)
            
            # when single text node is larger than max_size
            if text_size > max_size:
                if chunk:
                    chunks.append("\n".join(chunk))
                    chunk, chunk_size = [], 0
                # recursively split this big single node
                nodes = metta_ast_parser.parse(text_node)[0]
                subChunks = ChunkCodeRecursively(nodes, text_node, max_size)
                chunks.extend(subChunks)

            # when adding this text node exceeds max_size
            elif chunk_size + text_size > max_size:
                if chunk:
                    chunks.append("\n".join(chunk))
                chunk, chunk_size = [], 0
            else:
                chunk.append(text_node)
                chunk_size += text_size

        if chunk:
            chunks.append("\n".join(chunk))

    return chunks

def ChunkCode(code: str, max_size: int) -> List[str]:
    """
    Chunks the code into smaller pieces based on the max_size.
    Stores the chunks in the database.
    """

    load_dotenv() 
    with psycopg.connect(os.getenv("POSTGRES_URL")) as conn:    
        db = DB(conn)
        db.recreate_schema()
        db.clear_text_nodes()
        db.clear_symbols()
        
        # for now lets pass the code to the chunker
        # later we can add a feature to fetch the source code from the db using the file_path
        potential_chunks = preprocess_code(code, "temp_path", db)
        chunks = ChunkPreprocessedCode(potential_chunks, max_size, db, code)
        ids = db.insert_chunks(chunks)
        return chunks

def ChunkCodeRecursively(node: metta_ast_parser.SyntaxNode ,text: str, max_size: int) -> list[str]:
    """Recursively chunks a potential chunk (syntax node) when it exceeds max_size."""
    if getSize(node) <= max_size:
        st, en = node.src_range
        return [text[st:en]]

    # No children to recurse into, accept oversized node
    if not node.sub_nodes:  
        st, en = node.src_range
        return [text[st:en]]

    chunks = []
    for sub_node in node.sub_nodes:
        sub_chunks = ChunkCodeRecursively(sub_node, text, max_size)
        if chunks and len(chunks[-1]) + len(sub_chunks[0]) <= max_size:
                chunks[-1] += "\n" + sub_chunks[0]
                sub_chunks = sub_chunks[1:]

        chunks.extend(sub_chunks)
    return chunks


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
    except FileNotFoundError:
        print(f"Error: Input file not found at '{args.input_file}'")
        return

    print(f"Chunking code with MAX_SIZE = {args.max_size}...")
    final_chunks = ChunkCode(source_code, args.max_size)
    print(final_chunks)
    print("Chunks Stored in database")
    print("Chunking complete!")

if __name__ == "__main__":
    main()
