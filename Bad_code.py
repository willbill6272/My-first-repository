import random

def math_pm(a, b):
    # Renamed slightly to avoid shadowing anything built-in
    return (a + b, a - b)

# Initialize 'a' just in case they fail the input
a = None

try:
    print(f"iq tester! average iq is {int(random.triangular(98, 102, 100))}") 
    user_input = input("what is 898988+79797789//6**7? ")
    a = int(user_input)
# Check the conditions using '=='
    if a == 899273:
        print(f"your iq is {int(random.triangular(100, 120, 110))}")
    elif a in math_pm(899273, 100): 
    # Checking if they missed it by +/- 100
        print("your iq is 97")
    else:
        print("your iq is 80")
except Exception as e:
    print(f"error: {e}\nyour iq is [error]")
