def remove_from_alphabet(list_of_letters): 
    alphabet = "abcdefghijklmnopqrstuvwxyz"
    for a in alphabet: 
        if a in list_of_letters:
            alphabet = alphabet.replace(a, "")

    return alphabet

print(remove_from_alphabet(['a', 'c', 't', 'z']))