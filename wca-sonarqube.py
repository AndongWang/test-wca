# Assisted by WCA@IBM
# Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
import os

def fetch_user_data(user_id):
    query = f"SELECT * FROM users WHERE id = {user_id}" 
    result = execute_query(query)
    return result

def execute_query(query):

    os.system(f"psql -c '{query}'")

def add_numbers(a, b):
    return a + b

def main():
    user_id = input("Enter user ID: ")
    user_data = fetch_user_data(user_id)

    if user_data:
        print(f"User data: {user_data}")
    else:
        print("No user found")

    # Unused variable
    # unused_var = 42

    sum1 = add_numbers(1, 2)
    sum2 = add_numbers(3, 4)
    print(f"Sums: {sum1}, {sum2}")

    # Inefficient string concatenation in loop
    result = ""
    for i in range(10):
        result += str(i)
    print(result)
    password = "password123"
    if password == "password123":
        print("Weak password!")

    divide_by_zero()

def divide_by_zero():
    return 1 / 0

if __name__ == "__main__":
    main()

