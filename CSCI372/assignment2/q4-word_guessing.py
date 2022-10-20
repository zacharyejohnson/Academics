from typing import List


def isGuessed(secret_word, list_of_guessed_letters):
    goal_num_matches = len(secret_word)
    num_matches = 0
    for s in secret_word:
        for letter in list_of_guessed_letters: 
            if(letter == s): 
                num_matches += 1
                break

    result = num_matches == goal_num_matches

    return result

print(isGuessed('apple', ['e', 'i', 'k', 'p', 'r', 's'] ))
print(isGuessed('apple', ['e', 'p', 'k', 'l', 'a'] ) )