import time
# program will delay execution slightly throughout to give the appearance of heavy-duty calculations

# total cost of dream home
total_cost = float (input("Please enter the cost of your dream home: "))

time.sleep(0.25)
# down payment required: 25% of total cost 
portion_down_payment = 0.25 
print("assuming a down payment of 25%")

time.sleep(0.25)
# current accrued savings 
current_savings = 0
print("assuming zero savings")

time.sleep(0.25)
# annual return on investment 
r = 0.04
print("assuming an annual return on investment of 4%")

time.sleep(0.25)
# annual salary
annual_salary = float (input("What is your annual salary?: "))
monthly_salary = annual_salary / 12

time.sleep(0.25)
# portion of salary saved
portion_saved = float (input("What proportion of your yearly salary will you save?: "))

time.sleep(0.25)

#calculations to find number of months 
num_months = 0
savings = 0
monthly_r = (1 + r)**(1/12)

while(savings < (portion_down_payment * total_cost)): 
    savings = ((portion_saved*monthly_salary)*num_months)**((1 + r)**(num_months/12))
    num_months += 1

print(f"It will take {num_months} months of saving for your dream home")



