print("Your password should contain more than 10 characters")
print("Your password MUST contain numbers, letters(a-z,A-Z), numbers and symbols(!,@,#, etc.)!")

import string
import random
character = string.ascii_letters + string.digits + string.punctuation
if length < 10:
    print("Warning: password is short and might not be secure.")
password = ''.join(random.choice(character)for _ in rang(length))
print("Your secure password is:",password)

length = int(input("Enter the desired password length:"))

