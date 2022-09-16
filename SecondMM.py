#Eshaan Vora
#EshaanVora@gmail.com
#Higher Order Markov Models

#This program implements and trains a markov model to print a randomized song for a singer, given previous lyrics from the singer

#Results are printed to console and saved to the 'results.txt' file

import string
import random
import numpy as np

#Initialize dictionaries for counting 1-word, 2-word, and 3-word sequences
countWords = {}
countFirstOrder = {}
countSecondOrder = {}

#Initialize dictionaries for storing probabilities in first-order and second-order models
first_model = {}
second_model = {}

file = open('lyrics/lin-manuel-miranda.txt', 'r')
nursery_rhymes = file.read()

#Convert all text to lowercase
nursery_rhymes = nursery_rhymes.lower()

#Remove punctuation from file using translate api
nursery_rhymes = nursery_rhymes.translate(str.maketrans('','', string.punctuation))

#Split file into individual words; returned as list
nursery_rhymes = nursery_rhymes.split()

#Iterate through text file; initialize and populate dictionaries; count 1,2,3 word sequences
for index, word in enumerate(nursery_rhymes):
    #Fill nested dictionaries so key will exist when trying to insert value later
     countSecondOrder[word] = {}
     countFirstOrder[word] = {}
     first_model[word] = {}
     second_model[word] = {}

     if nursery_rhymes[index] in countWords:
         countWords[word] += 1
     else:
         countWords[word] = 1

#Store 2-word sequences in "countFirstOrder" dictionary or update the count if the word is not unique
for index, word in enumerate(nursery_rhymes):
    if index == len(nursery_rhymes) - 1:
        break
    else:
        #Create dictionary to store first-order probabilities
        first_model[word][nursery_rhymes[index+1]] = {}
        #Fill nested dictionary so key will exist when trying to insert value later
        second_model[word][nursery_rhymes[index+1]] = {}
        countSecondOrder[word][nursery_rhymes[index+1]] = {}

        if nursery_rhymes[index+1] in countFirstOrder[word]:
            countFirstOrder[word][nursery_rhymes[index+1]] += 1
        else:
            countFirstOrder[word][nursery_rhymes[index+1]] = 1

#Store 3-word sequences in "countSecondOrder" dictionary or update the count if the word is not unique
for index, word in enumerate(nursery_rhymes):
    if index == len(nursery_rhymes) - 2:
        break
    else:
        #Create dictionary to store second-order probabilities
        second_model[word][nursery_rhymes[index+1]][nursery_rhymes[index+2]] = 0

        if nursery_rhymes[index+2] in countSecondOrder[word][nursery_rhymes[index+1]]:
            countSecondOrder[word][nursery_rhymes[index+1]][nursery_rhymes[index+2]] += 1
        else:
            countSecondOrder[word][nursery_rhymes[index+1]][nursery_rhymes[index+2]] = 1

#Generate 1st Order Markov Model
for word in first_model:
    for secondWord in first_model[word]:
        first_model[word][secondWord] = countFirstOrder[word][secondWord] / countWords[word]

#Generate 2nd Order Markov Model
for word in second_model:
    for secondWord in second_model[word]:
        for thirdWord in second_model[word][secondWord]:
            second_model[word][secondWord][thirdWord] = countSecondOrder[word][secondWord][thirdWord] / countFirstOrder[word][secondWord]

#Ensure first-order and second-order models have been trained correctly
#print(first_model)
#print(second_model)

#Generate random first word
first_word = nursery_rhymes[random.randint(0, len(nursery_rhymes)-1)]

#Generate random second word based on probabilities of the possible next words from first-order Markov model "first_model"
second_word_possibilities = []
second_word_prob = []
for word in first_model[first_word]:
    second_word_possibilities.append(word)
    second_word_prob.append(first_model[first_word][word])

second_word = np.random.choice(second_word_possibilities, 1, second_word_prob)[0]

#Append word to phrase based on previous 2 words
phrase = " " + first_word + " " + second_word

#Generate remaining words based on probabilities of the possible next words from second-order Markov model "second_model"
#Already have first and second word, so we must generate 598 additional words; (30 lines x 20 words = 600 total words needed)
i = 0
while i < 598:
    next_word_possibilities = []
    next_word_prob = []
    for word in second_model[first_word][second_word]:
        next_word_possibilities.append(word)
        next_word_prob.append(second_model[first_word][second_word][word])
        next_word = np.random.choice(next_word_possibilities, 1, next_word_prob)[0]

    phrase += " " + next_word

    #Split line after every 20 words
    if len(phrase.split()) % 20 == 0:
        phrase += "\n"

    #Update state before next iteration
    first_word = second_word
    second_word = next_word
    i += 1

print(phrase)

f = open("results.txt", "w")
f.write(phrase)
f.close()
