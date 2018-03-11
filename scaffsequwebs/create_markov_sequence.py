
"""
Functionality to generate markov-Sequences
of different order
"""
import random

DNA_letters = ['A','C','G','T']

class MarkovSequence:
    def __init__(self,markov_order):
        self.__order = markov_order
    def CreateFirstOrderSequence(self,length):
        self.__length = length
        self.__sequ = ""
        for i in range(self.__length):
            self.__sequ+=random.choice(DNA_letters)
        return self.__sequ

if __name__ == "__main__":
    ms = MarkovSequence(5)
    sequ = ms.CreateFirstOrderSequence(2000)
    print(sequ)

    #def __str__(self):
