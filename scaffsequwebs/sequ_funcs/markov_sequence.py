
"""
Functionality to generate markov-Sequences
of different order
"""
if __name__ == "__main__":
	from dna_sequence import CDNASequence
else:
	from .dna_sequence import CDNASequence
import random

DNA_letters = ['A','C','G','T']

class CMarkovSequence(CDNASequence):
    def __init__(self,markov_order):
        CDNASequence.__init__(self)
        self.__order = markov_order
    def CreateFirstOrderSequence(self,length):
        self.__length = length
        self._sequ = ""
        for i in range(self.__length):
            self._sequ+=random.choice(DNA_letters)
    def TrainMarkovModel(self,train_sequ,is_linear=True):
        """ take as an input a sequence and create
            a dictionary, with all the sequs of length
            markov_order as keys and the following letters
            as values
        """
        #print("TRAINING A MARKOV MODEL")
        self.__train_sequ = train_sequ
        if is_linear:
            self.__train_sequ+=train_sequ[0]

        self.__string_dict = dict()

        for i in range(len(train_sequ)-self.__order):
            curr_keystring = train_sequ[i:i+self.__order]
            curr_valuechar = train_sequ[i+self.__order]
            if curr_keystring in self.__string_dict:
                self.__string_dict[curr_keystring].append(curr_valuechar)
            else:
                self.__string_dict[curr_keystring]=list()
                self.__string_dict[curr_keystring].append(curr_valuechar)

    def CreateSequenceFromTrainedModel(self,length):
        """ generate a Markov sequence of order "self.__order" and length "length"
            this method has to be called after calling the "TrainMarkovModel" - method
            1.
            TrainMarkovModel(train_sequ)
            2.
        """
        self.__length = length
        self._sequ=""
        train_sequ_len = len(self.__train_sequ)
        ## randomly (uniformly) choose a starting tuple from the sequence:
        index_start_tuple = random.randint(0,train_sequ_len-self.__order-1)
        initial_tuple = self.__train_sequ[index_start_tuple:(index_start_tuple+self.__order)]
        self._sequ = initial_tuple
        curr_key = initial_tuple
        for i in range(self.__length-self.__order):
            next_letter=random.choice(self.__string_dict[curr_key])
            self._sequ+=next_letter
            next_key = curr_key[1:len(curr_key)]+next_letter
            curr_key = next_key







            #rint("curr keystring: " + curr_keystring + " curr valuechar: " + curr_valuechar)



if __name__ == "__main__":
    train_sequ = "AGCTTGGCACTGGCCGTCGTTTTACAACGTCGTGACTGGGAAAACCCTGGCGTTACCCAACTTAATCGCCTTGCAGCACATCCCCCTTTCGCCAGCTGGCGTAATA"
    ms = CMarkovSequence(2)
    ms.TrainMarkovModel(train_sequ)
    ms.CreateSequenceFromTrainedModel(7560)
    sequ = ms.GetSequence()
    print(sequ)


    #def __str__(self):
