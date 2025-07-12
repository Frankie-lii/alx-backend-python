#!/usr/bin/env python3

import time
import sqlite3 
import functools

# Global cache dictionary
query_cache = {}

# --- Decorator to handle DB connection ---
def with_db_connection(func):
        @functools.wraps(func)
            def wrapper(*args, **kwargs):
                        conn = sqlite3.connect('users.db')
                                try:
                                                return func(conn, *args, **kwargs)
                                                    finally:
                                                                    conn.close()
                                                                        return wrapper

                                                                    # --- Decorator to cache query results ---
                                                                    def cache_query(func):
                                                                            @functools.wraps(func)
                                                                                def wrapper(conn, *args, **kwargs):
                                                                                            query = kwargs.get('query') if 'query' in kwargs else (args[0] if args else '')
                                                                                                    if query in query_cache:
                                                                                                                    print(f"[CACHE] Using cached result for query: {query}")
                                                                                                                                return query_cache[query]
                                                                                                                                    print(f"[DB] Executing and caching query: {query}")
                                                                                                                                            result = func(conn, *args, **kwargs)
                                                                                                                                                    query_cache[query] = result
                                                                                                                                                            return result
                                                                                                                                                            return wrapper

                                                                                                                                                        @with_db_connection
                                                                                                                                                        @cache_query
                                                                                                                                                        def fetch_users_with_cache(conn, query):
                                                                                                                                                                cursor = conn.cursor()
                                                                                                                                                                    cursor.execute(query)
                                                                                                                                                                        return cursor.fetchall()

                                                                                                                                                                    # --- First call: hits DB and caches
                                                                                                                                                                    users = fetch_users_with_cache(query="SELECT * FROM users")

                                                                                                                                                                    # --- Second call: uses cached result
                                                                                                                                                                    users_again = fetch_users_with_cache(query="SELECT * FROM users")

                                                                                                                                                                    # Optional: print results
                                                                                                                                                                    print(users_again)

