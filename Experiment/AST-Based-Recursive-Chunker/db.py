from pymongo import AsyncMongoClient

class Database:
    def __init__(self,url,db_name="MeTTa_chunks"):
        self.client = AsyncMongoClient(url)
        self.db = self.client.get_database(db_name)

        # get collections
        self.text_nodes = self.db["text_nodes"]
        self.symbols = self.db["symbols"]
        self.chunks = self.db["chunks"]
    
    async def clear_text_nodes_symbols(self):
        """
        clear these collections after a function scope is processed
        to avoid duplicate key errors on processing same function names 
        in different scopes
        """
        await self.text_nodes.delete_many({})
        await self.symbols.delete_many({})
    
    async def clear_all_collections(self):
        """Clear all collections development only."""
        await self.text_nodes.delete_many({})
        await self.symbols.delete_many({})
        await self.chunks.delete_many({})

    async def close(self):
        await self.client.close()
    
    #----------------------------
    # TEXT_NODES CRUD
    #----------------------------
    async def insert_text_node(self, text_range: tuple[int, int], file_path: str, node_type: str) -> int:
        """Insert a new text_node document."""
        doc = {
            "text_range": text_range,
            "file_path": file_path,
            "node_type": node_type
        }
        result = await self.text_nodes.insert_one(doc)
        return result.inserted_id

    async def get_text_node(self, node_id: int):
        """Fetch a text_node document by ID."""
        result = await self.text_nodes.find_one({"_id": node_id})
        if result:
            return result
        return "Text node not found"

    #----------------------------
    # SYMBOLS CRUD
    #----------------------------
    async def upsert_symbol(self, name: str, col: str, node_id: int):
        """Add a node_id to the given symbol's column (defs, calls, asserts, types)."""
        update = {"$addToSet": {col: node_id}}
        result = await self.symbols.update_one({"name": name}, update, upsert=True)
        return result.upserted_id if result.upserted_id else None

    async def get_symbol(self, name: str):
        """Fetch a symbol document by name."""
        result = await self.symbols.find_one({"name": name})
        if result:
            return result
        return "Symbol not found"
    
    async def get_all_symbols(self):
        """Return all documents from the symbols collection."""
        results = []
        async for doc in self.symbols.find({}):
            results.append(doc)
        return results
    
    #----------------------------
    # CHUNKS CRUD
    #----------------------------
    async def insert_chunk(self, chunk_text: str) -> int:
        """Insert a single chunk_text document. Returns the inserted ID."""
        doc = {
            "chunk_text": chunk_text
        }
        result = await self.chunks.insert_one(doc)
        return result.inserted_id
    
    async def insert_chunks(self, chunk_texts: list[str]) -> list[int]:
        """
        Insert multiple chunk_text documents at once.
        Returns a list of inserted IDs in the same order as input.
        """
        if not chunk_texts:
            return []
        docs = [{"chunk_text": text} for text in chunk_texts]
        result = await self.chunks.insert_many(docs)
        return result.inserted_ids

    async def get_chunk(self, chunk_id: int):
        """Fetch a chunk document by ID."""
        result = await self.chunks.find_one({"_id": chunk_id})
        if result:
            return result
        return "Chunk not found"

    async def get_all_chunks(self):
        """Return all documents from the chunks collection."""
        results = []
        async for doc in self.chunks.find({}):
            results.append(doc)
        return results
