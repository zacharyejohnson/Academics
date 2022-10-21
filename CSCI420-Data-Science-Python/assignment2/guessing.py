import random

rand_num = random.randint(1, 10)

for i in range(5): 
    num = int (input("please enter your integer guess: "))
    if num == rand_num: 
        print(f"Congratulations! You guessed the number in {i+1} attempts")
        break
    elif num > rand_num:
        print("Your number is too high. Try again.") 
    elif num < rand_num:
        print("Your number is too low.  Try again.")
    elif i == 4: 
        print("Sorry you failed")