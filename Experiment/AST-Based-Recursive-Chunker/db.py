class Database:
    def __init__(self, conn):
        self.conn = conn

    def create_tables(self):
        """Create tables from schema if they don't exist."""

        schema = ["""
        CREATE TABLE IF NOT EXISTS text_nodes (
            id SERIAL PRIMARY KEY,
            text_range INTEGER[2] NOT NULL,
            file_path TEXT NOT NULL,
            node_type TEXT NOT NULL
        );""",
        """
        CREATE TABLE IF NOT EXISTS symbols (
            id SERIAL PRIMARY KEY,
            name TEXT NOT NULL,
            defs INTEGER[],
            calls INTEGER[],
            asserts INTEGER[],
            types INTEGER[]
        );""",
        """
        CREATE TABLE IF NOT EXISTS chunks (
            id SERIAL PRIMARY KEY,
            chunk_text TEXT NOT NULL
        );
        """]

        with self.conn.cursor() as cur:
            for stmt in schema:
                cur.execute(stmt)
            self.conn.commit()
    
    def drop_all_tables(self):
        """Only for development: drop all project tables."""
        with self.conn.cursor() as cur:
            cur.execute("DROP TABLE IF EXISTS chunks, symbols, text_nodes CASCADE;")
        self.conn.commit()

    def recreate_schema(self):
        """Only for development: drop all tables and recreate schema."""
        self.drop_all_tables()
        self.create_tables()

    # ----------------------------
    # TEXT_NODES CRUD
    # ----------------------------
    def insert_text_node(self, text, file_path, node_type):
        """Insert a new text_node row."""

        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO text_nodes (text_range, file_path, node_type) VALUES (%s, %s, %s) RETURNING id",
                (text, file_path, node_type),
            )
            node_id = cur.fetchone()[0]
            self.conn.commit()
            return node_id

    def get_text_node(self, node_id):
        """Fetch a text_node row by ID."""

        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM text_nodes WHERE id = %s", (node_id,))
            return cur.fetchone()
    
    def clear_text_nodes(self):
        """Delete all rows from the text_nodes table."""

        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM text_nodes")
            self.conn.commit()

    # ----------------------------
    # SYMBOLS CRUD
    # ----------------------------
    def upsert_symbol(self, name, col, node_id):
        """Add a node_id to the given symbol's column (defs, calls, asserts, types)."""

        with self.conn.cursor() as cur:
            # Check if symbol exists
            cur.execute("SELECT id FROM symbols WHERE name = %s", (name,))
            row = cur.fetchone()

            if row:
                # Update array by appending
                query = f"UPDATE symbols SET {col} = array_append({col}, %s) WHERE name = %s"
                cur.execute(query, (node_id, name))
            else:
                # Insert with only one array populated
                col_dict = {
                    "defs": "ARRAY[]::integer[]",
                    "calls": "ARRAY[]::integer[]",
                    "asserts": "ARRAY[]::integer[]",
                    "types": "ARRAY[]::integer[]"
                }
                col_dict[col] = f"ARRAY[{node_id}]"
                cur.execute(
                    f"INSERT INTO symbols (name, defs, calls, asserts, types) VALUES (%s, {col_dict['defs']}, {col_dict['calls']}, {col_dict['asserts']}, {col_dict['types']})",
                    (name,),
                )
            self.conn.commit()

    def get_symbol(self, name):
        """Fetch a symbol row by name."""

        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM symbols WHERE name = %s", (name,))
            return cur.fetchone()
        
        self.conn.commit()
    
    def get_all_symbols(self):
        """Return all rows from the symbols table."""

        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM symbols")
            return cur.fetchall()

    def clear_symbols(self):
        """Delete all rows from the symbols table."""

        with self.conn.cursor() as cur:
            cur.execute("DELETE FROM symbols")
            self.conn.commit()
    

    # ----------------------------
    # CHUNKS CRUD
    # ----------------------------
    def insert_chunk(self, chunk_text):
        """Insert a single chunk_text row. Returns the inserted ID."""

        with self.conn.cursor() as cur:
            cur.execute(
                "INSERT INTO chunks (chunk_text) VALUES (%s) RETURNING id",
                (chunk_text,),
            )
            chunk_id = cur.fetchone()[0]
            self.conn.commit()
            return chunk_id
    
    def insert_chunks(self, chunk_texts):
        """
        Insert multiple chunk_text rows at once.
        Returns a list of inserted IDs in the same order as input.
        """
        if not chunk_texts:
            return []
        with self.conn.cursor() as cur:
            cur.execute(
                """
                INSERT INTO chunks (chunk_text)
                SELECT unnest(%s::text[])
                RETURNING id
                """,
                (chunk_texts,),
            )
            ids = [row[0] for row in cur.fetchall()]
            self.conn.commit()
            return ids

    def get_chunk(self, chunk_id):
        """Fetch a chunk row by ID."""

        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM chunks WHERE id = %s", (chunk_id,))
            return cur.fetchone()
    
    def get_all_chunks(self):
        """Return all rows from the chunks table."""

        with self.conn.cursor() as cur:
            cur.execute("SELECT * FROM chunks")
            return cur.fetchall()
