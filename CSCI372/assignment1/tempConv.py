# tempConv.py 
# Zach Johnson CSCI372 Assignment 1
# creates a conversion object which can convert
# only celsius and fahrenheit at the moment but more conversions could easily be added

deg_celsius = input("please provide a degrees celsius: ")
def celsius_to_fahrenheit(deg_celsius): 
        deg_fahenheit = (float)(deg_celsius) * ((float)(9)/(float)(5)) +32
        return print("%s degrees celsius is %d degrees fahrenheit" %((deg_celsius), deg_fahenheit))

celsius_to_fahrenheit(deg_celsius)


