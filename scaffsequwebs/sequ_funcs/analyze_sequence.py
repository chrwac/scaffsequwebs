""" functionality to analyze
DNA scaffold-sequences
"""
DNA_letters = ['A','C','G','T']

class SequenceAnalyzer:
    def __init__(self,sequ):
        self.__sequ = sequ
    def CountLetters(self):
        self.__lettercount = dict()
        for i in DNA_letters:
            self.__lettercount[i] = 0
        for i in self.__sequ:
            self.__lettercount[i]+=1
        self.__num_letters = sum(self.__lettercount.values())

        return self.__lettercount
    def GetCGContent(self):
        self.__cgcontent=(float(self.__lettercount['C'])+float(self.__lettercount['G']))/float(self.__num_letters)
        return(self.__cgcontent)
