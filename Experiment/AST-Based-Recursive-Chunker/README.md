# Chunking

The goal of selecting the best chunking strategy is to make each chunk as meaningful and complete as possible.  
Semantically similar code should stay together so that a chunk represents a full, coherent unit.  
This is our final goal.

Any vector store requires chunking large documents for effective search.

> Further reading: Design Notes [docs/design-notes.md](docs/design-notes.md)

---

## What’s new in this iteration

- AST-driven + symbol-aware chunking:
  - We still parse MeTTa into an AST, but now add a middle layer that aggregates code by symbol (defs, types, asserts, calls) before chunking.
- Recursive splitting for oversized nodes (preserves semantics while fitting size).
- PostgreSQL backend:
  - text_nodes: stores source ranges + file_path (no duplicate text).
  - symbols: arrays of text_node IDs grouped by symbol.
  - chunks: stores the final chunk text.
- Dev-only schema reset (optional) to iterate quickly on schema changes.

---

## Why not store whole files in vector databases?

- Context windows of models are limited.
- Smaller & concise chunks better match specific queries and avoid noise.
- Ideal strategy: use the smallest chunk that still contains all relevant context.

---

## Suitable Chunk Size for Open Source Model Context Windows

- Current open-source LLMs have context windows ~512–1500 tokens.
- Approximate ratio: 1 token ≈ 5 characters.
- To fit within windows, chunk size ≈ 1500–6500 characters (excluding prompt tokens).

---

## How can we chunk code files?

There are 4 main strategies:

1. Heuristic (fixed size)  
2. Rule-based (using delimiters)  
3. Overlapping (sliding window)  
4. Syntax-aware chunking (AST-based)

Problems with the first two:
- Heuristic & rule-based approaches ignore semantics and split code incorrectly.

Our approach: Syntax-aware + symbol-aware chunking
- Parse into an AST for structure.
- Middle layer aggregates related code by head symbol (defs, types, asserts, calls).
- Chunk the aggregated groups, recursively splitting only when size requires.

Steps:
1. Generate AST structure.
2. Build symbol index (defs/types/asserts/calls).
3. Chunk groups under a max size with recursive splitting for large nodes.

---

## Architecture Overview

1. Parse MeTTa file → AST.
2. Extract head symbols per relevant node.
3. Persist nodes into text_nodes (text_range + file_path + node_type).
4. Update symbols table with node IDs grouped by name (defs, calls, asserts, types).
5. Preprocess → build potential chunks by symbol association.
6. Chunking:
   - Merge related nodes into chunks up to max_size.
   - If a node is too large, split recursively by its sub-nodes.
7. Store final chunks (chunk_text) in Postgres.

---

## Database Schema (dev)

- text_nodes
  - id SERIAL PRIMARY KEY
  - text_range INTEGER[2] NOT NULL  (start, end character offsets)
  - file_path TEXT NOT NULL          (currently a demo path; repo parsing next)
  - node_type TEXT NOT NULL          (rule, call, type, assert, comment, …)

- symbols
  - id SERIAL PRIMARY KEY
  - name TEXT NOT NULL
  - defs INTEGER[]
  - calls INTEGER[]
  - asserts INTEGER[]
  - types INTEGER[]
  (arrays hold text_node IDs)

- chunks
  - id SERIAL PRIMARY KEY
  - chunk_text TEXT NOT NULL

---

## Getting the Best Out of Chunks

- Denoising: keep the smallest relevant chunk.
- Coalescing: remove whitespace.
- Handle deep/large code via recursive splitting and reconstruction.
- If a single syntax node exceeds context window → split recursively.
- Dynamic chunk sizing: tune for model limits.
- Optional overlap to improve retrieval coverage.
- Enhanced embeddings: add natural language descriptions.

Note: When embedding, store both vectors + raw chunks.

---

## Strategies for Large Code Repositories

- Repo-level filtering: focus on “golden repos”.
- Selective parsing: only MeTTa files.
- Different splitters: docs vs code.
- Next: traverse repos and persist true file_path (we currently use a demo path).

---

## Large Scale Data Ingestion Pipeline Plan

![Ingest pipeline](docs/ingest-pipeline.png)

---

## Problems and Ongoing Work

- MeTTa parser lacked richer node types; we extended groups:
  - ExpressionGroup, CallGroup, RuleGroup, TypeCheckGroup.
- Remaining work:
  - Repository-level traversal and cross-file symbol aggregation.
  - Indexing/constraints for faster lookups and integrity.
  - Optional source maps for traceability.

---

## Configuration

Create a .env:

```env
POSTGRES_URL=postgresql://postgres:password@localhost:5433/metta_chunks
```

---

## Running the Chunker

```bash
# Create virtual environment
python -m venv .venv
source .venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Normal run
python chunker.py [input_file_path] [output_file_path] --max-size 1500
```

Outputs:
- Chunked code stored in DB (chunks table).
- Related defs/types/asserts/calls grouped by symbol.
- Oversized nodes recursively split while preserving semantics.

---

## Resources

- Chunking 2M Files (Sweep Docs, archived)  
  https://web.archive.org/web/20240413093103/https://docs.sweep.dev/blogs/chunking-2m-files
- RAG For a Codebase with 10k Repos  
  https://www.qodo.ai/blog/rag-for-large-scale-code-repos/
- cAST: Enhancing Code Retrieval-Augmented Generation with Structural Chunking via Abstract Syntax Tree  
  https://arxiv.org/pdf/2506.15655
- DataCamp: PostgreSQL + Python Tutorial  
  https://www.datacamp.com/tutorial/tutorial-postgresql-python
- Building Python Apps with PostgreSQL and psycopg3 (TigerData)  
  https://www.tigerdata.com/learn/building-python-apps-with-postgresql
- Symbol Table in compilers
  https://www.geeksforgeeks.org/compiler-design/symbol-table-compiler