#!/usr/bin/env python3

import asyncio
import aiosqlite

DB_NAME = "users.db"

# Fetch all users
async def async_fetch_users():
        async with aiosqlite.connect(DB_NAME) as db:
                    async with db.execute("SELECT * FROM users") as cursor:
                                    rows = await cursor.fetchall()
                                                print("All Users:")
                                                            for row in rows:
                                                                                print(row)

                                                                                # Fetch users older than 40
                                                                                async def async_fetch_older_users():
                                                                                        async with aiosqlite.connect(DB_NAME) as db:
                                                                                                    async with db.execute("SELECT * FROM users WHERE age > ?", (40,)) as cursor:
                                                                                                                    rows = await cursor.fetchall()
                                                                                                                                print("\nUsers older than 40:")
                                                                                                                                            for row in rows:
                                                                                                                                                                print(row)

                                                                                                                                                                # Run both queries concurrently
                                                                                                                                                                async def fetch_concurrently():
                                                                                                                                                                        await asyncio.gather(
                                                                                                                                                                                        async_fetch_users(),
                                                                                                                                                                                                async_fetch_older_users()
                                                                                                                                                                                                    )

                                                                                                                                                                        # Run the concurrent tasks
                                                                                                                                                                        if __name__ == "__main__":
                                                                                                                                                                                asyncio.run(fetch_concurrently())

