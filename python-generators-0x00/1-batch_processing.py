#!/usr/bin/env python3

import mysql.connector

# ---------- Stream users in batches ----------
def stream_users_in_batches(batch_size):
        connection = mysql.connector.connect(
                        host="localhost",
                                user="root",
                                        password="your_password",  # Replace with your MySQL root password
                                                database="ALX_prodev"
                                                    )

            cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM user_data")

                    while True:
                                batch = cursor.fetchmany(batch_size)
                                        if not batch:
                                                        break
                                                            yield batch  # Yield one batch at a time

                                                                cursor.close()
                                                                    connection.close()

                                                                    # ---------- Process batches and filter users over age 25 ----------
                                                                    def batch_processing(batch_size):
                                                                            for batch in stream_users_in_batches(batch_size):  # loop 1
                                                                                        filtered_batch = [user for user in batch if float(user['age']) > 25]  # loop 2 (list comp counts as 1 loop)
                                                                                                yield filtered_batch  # Yield filtered users

