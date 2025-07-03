#!/usr/bin/env python3

import mysql.connector

def stream_users():
        connection = mysql.connector.connect(
                        host="localhost",
                                user="root",
                                        password="your_password",  # replace with your MySQL password
                                                database="ALX_prodev"
                                                    )

            cursor = connection.cursor(dictionary=True)
                cursor.execute("SELECT * FROM user_data")

                    for row in cursor:
                                yield row  # Stream one row at a time

                                    cursor.close()
                                        connection.close()

