# Google EmbeddingGemma Code Search

This project demonstrates an interactive code search system built with Google's EmbeddingGemma model. It compares three different embedding strategies to determine the most effective method for retrieving relevant code snippets based on a natural language query.

## Methodology

We evaluated the performance of three distinct embedding strategies:

1.  **Code-Only:** The model creates an embedding based solely on the function's code.
2.  **Code + Description (Combined):** The function's code and its natural language description are joined into a single string and then embedded.
3.  **Code + Description (Separate):** Separate embeddings are generated for the code and the description. The final similarity score is a weighted average of the two individual scores.

## Key Findings

Our analysis found that the **Code + Description (Combined)** strategy consistently outperforms the other two approaches.

This success can be attributed to the fact that the combined approach provides the model with a richer, more comprehensive context. By embedding both the structural logic of the code and the conceptual explanation from its natural language description, the model is able to better align the user's query with the function's overall purpose, leading to more accurate and relevant search results.

## Conclusion

The results show that integrating natural language descriptions with code is the most effective method for building a high-performance semantic code search system with the EmbeddingGemma model. This highlights the significant value of having well-documented code for retrieval tasks.