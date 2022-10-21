def letter_appearances(string):
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    appearances_dict = {}
    for a in alphabet:
        appearances = 0 
        for s in string:
            if(a == s):
                appearances += 1
        appearances_dict[a] = appearances

    print("String: " + string)

    print("LETTER", "APPEARANCES")

    for key, val in appearances_dict.items(): 
        print(key + ": " +str(val))


letter_appearances('potatoes')


