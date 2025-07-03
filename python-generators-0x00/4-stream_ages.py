#!/usr/bin/env python3

import mysql.connector

# --------- Generator that streams user ages one by one ---------
def stream_user_ages():
        connection = mysql.connector.connect(
                        host="localhost",
                                user="root",
                                        password="your_password",  # Replace with your MySQL password
                                                database="ALX_prodev"
                                                    )

            cursor = connection.cursor()
                cursor.execute("SELECT age FROM user_data")

                    for (age,) in cursor:  # Loop 1
                                yield float(age)

                                    cursor.close()
                                        connection.close()

                                        # --------- Compute average age using the generator ---------
                                        def compute_average_age():
                                                total = 0
                                                    count = 0

                                                        for age in stream_user_ages():  # Loop 2
                                                                    total += age
                                                                            count += 1

                                                                                if count == 0:
                                                                                            print("No users found.")
                                                                                                else:
                                                                                                            average = total / count
                                                                                                                    print(f"Average age of users: {average:.2f}")

                                                                                                                    # --------- Run the function ---------
                                                                                                                    if __name__ == "__main__":
                                                                                                                            compute_average_age()

