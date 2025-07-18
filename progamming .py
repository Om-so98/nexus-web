print("karibu!welcome to the age group checker!")
age =int(input("kindly enter your age:"))
if age <=0:
    print("invalid")
elif age < 5:
    print("You are a todler")
elif age <=12:
    print("you are a child")    
elif age <=17:
    print("you are a teenager")
elif age <=35:
    print("you are a youth")
elif age >=50:
    print("You are an adult")
else:
    print("you are a senior adult")




