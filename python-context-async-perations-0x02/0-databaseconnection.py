#!/usr/bin/env python3

import sqlite3

class DatabaseConnection:
        def __init__(self, db_name):
                    self.db_name = db_name
                            self.conn = None
                                    self.cursor = None

                                        def __enter__(self):
                                                    # Open the connection and return the cursor
                                                            self.conn = sqlite3.connect(self.db_name)
                                                                    self.cursor = self.conn.cursor()
                                                                            return self.cursor

                                                                            def __exit__(self, exc_type, exc_value, traceback):
                                                                                        # Commit changes if no exception, rollback if there was an error
                                                                                                if exc_type is not None:
                                                                                                                self.conn.rollback()
                                                                                                                        else:
                                                                                                                                        self.conn.commit()
                                                                                                                                                # Close the connection
                                                                                                                                                        self.conn.close()

                                                                                                                                                        # --- Usage Example ---
                                                                                                                                                        if __name__ == "__main__":
                                                                                                                                                                db_name = "users.db"

                                                                                                                                                                    with DatabaseConnection(db_name) as cursor:
                                                                                                                                                                                cursor.execute("SELECT * FROM users")
                                                                                                                                                                                        results = cursor.fetchall()
                                                                                                                                                                                                for row in results:
                                                                                                                                                                                                                print(row)

