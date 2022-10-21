import numpy as np 

def sqrt_bisection(n): 
    # minimum square root is 0 and maximum square root is n squared if the value is less than 1
    min = 0
    max = n

    midpoint = lambda x,y: (x+y)/2
    mid = midpoint(min, max)
    # our accuracy will be to 2 decimal places, generally a fair approximation that won't tax the computer too much
    while(mid*mid < n - 0.001 or mid*mid > n + 0.001):
        high = midpoint(mid, max)**2
        low = midpoint(min, mid)**2
        
        if(np.abs(high - n) < np.abs(low - n)):
            min = mid
            mid = midpoint(mid, max)
            max = max
        
        else: 
            max = mid
            mid = midpoint(min, mid)
            min = min

    return_string = f"the square root of {n} is ~{round(mid, 3)}"
    return return_string


array = np.arange(1, 6)

for a in array: 
    print(sqrt_bisection(a))
