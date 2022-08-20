import numbers

def prime_check(number):
 is_prime = True
 for i in range(2,number -1):
    if number % i == 0:
        is_prime=False
 if is_prime == True: 
    print("It's is Prime Number")
 else:
    print("It Not a Prime Number")



# n = int(input("check wheather the Number is Prime number : "))
prime_check(5)
prime_check(6)
prime_check(12)

