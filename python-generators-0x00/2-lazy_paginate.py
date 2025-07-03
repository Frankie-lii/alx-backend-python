#!/usr/bin/env python3

import mysql.connector

# --------- Fetch a single page of users with limit and offset ---------
def paginate_users(page_size, offset):
        connection = mysql.connector.connect(
                        host="localhost",
                                user="root",
                                        password="your_password",  # Replace with your actual password
                                                database="ALX_prodev"
                                                    )

            cursor = connection.cursor(dictionary=True)
                query = "SELECT * FROM user_data LIMIT %s OFFSET %s"
                    cursor.execute(query, (page_size, offset))
                        results = cursor.fetchall()

                            cursor.close()
                                connection.close()
                                    return results

                                # --------- Lazy pagination generator ---------
                                def lazy_paginate(page_size):
                                        offset = 0
                                            while True:  # Only one loop used
                                                        page = paginate_users(page_size, offset)
                                                                if not page:
                                                                                break
                                                                                    yield page
                                                                                            offset += page_size

