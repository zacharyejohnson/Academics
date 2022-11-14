def findPeakElements(nums): 
    peak = False
    # enumerate method will alow us to access list elements by both index and their value 
    for i, ele in enumerate(nums): 
        # conditions to ensure we dont get key error
        if i > 1 and i < len(nums) - 1: 
            if(nums[i-1] < nums[i] > nums[i + 1]): 
                peak = True
                return i
                break
    if not peak:
        print("No peaks found")
        
            


#test 
# This method returns just the first peak as the instructions were to return any peak 
# - please contact me if you would like this changed to include all peaks or the greatest peak 

a = [1,2,3,4,5,4,5,6,8,5,6,8,2]
b = [0,1,2,3,4,5]

print(findPeakElements(a))
print(findPeakElements(b))


