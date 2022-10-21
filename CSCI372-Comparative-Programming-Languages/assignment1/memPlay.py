a = "string"
b = "string"
def compareStrings(a, b):
    print(id(a), id(b))

compareStrings(a,b)

# the output suggest that indeed one string takes one spot in the systems memory and hence 
# if two variables have the same string value they are in fact the same object

print(a is b)
print(a == b)
