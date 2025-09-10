# MeTTa AST Parser

A **standalone Abstract Syntax Tree (AST) parser** for the MeTTa language, built for an integration with syntax-aware chunking algorithm.  
This parser is a key component of an AI coding assistant designed for **Retrieval-Augmented Generation (RAG)** over large MeTTa codebases.  

The parser is implemented in **Rust** for speed and safety, and exposed to **Python** for simple use in the data pipelines.

--- 

- Build a **lightweight AST parser** for MeTTa, independent from the full Hyperon execution engine.  
- Provide **structurally-aware parsing** to support chunking.  
- Enable Python integration.

---

## Source Code Foundations

The parser was developed after analyzing the **hyperon-experimental repo**, focusing on these files:

- **`text.rs`** → Core S-expression parser (`SExprParser`), syntax tree (`SyntaxNode`, `SyntaxNodeType`), tokenizer.  
- **`metta.rs`** → C-style enum definitions for node types → guided our Rust `SyntaxNodeType`.  
- **`metta_shim.rs`** → Example usage of `parse_to_syntax_tree()` in MeTTa REPL.  
- **`check_sexpr_parser.c` & `hyperonpy.cpp`** → Showed integration and Python bridge patterns.  

---

## Implementation Strategy

### 1. Core Rust Library
- Extracted `SExprParser`, `SyntaxNode`, `SyntaxNodeType` into `src/lib.rs`.  
- Removed dependencies on Hyperon’s atom-space & execution engine.  
- Added minimal stubs → parser only builds AST (no evaluation).  

### 2. Python Bridge (via PyO3 + maturin)
- Used **PyO3** to expose Rust structs to Python.  
- Annotated core objects (`SyntaxNode`, `SyntaxNodeType`) with `#[pyclass]`.  
- Defined getters (e.g. `node_type`, `src_range`).  
- Exposed main entrypoints

### 3. Refinements
- Multiple top-level expressions: aligned with metta_shim.rs behavior.
- MeTTa expression executor (!): added parse_exec_expression() to correctly parse !(...) blocks.