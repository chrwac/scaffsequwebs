""" functionality to analyze
DNA scaffold-sequences
"""
import re
from . import dna_sequence
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
    def GetListOfTuples(self,tuple_length=7):
        self.__tuples = list()
        for i in range(0,len(self.__sequ)-tuple_length+1):
            temp_tuple = self.__sequ[i:i+tuple_length];
            self.__tuples.append(temp_tuple);
        return self.__tuples
    def ContainsDuplicateTuples(self):
        if not self.__tuples:
            print("list of tuples has not yet been created")
            print("please call the method GetListOfTuples(tuple_length) first")
        else:
            if(len(self.__tuples)==len(set(self.__tuples))):
                return False;
            else:
                return True;
    def GetDictOfDuplicates(self):
        self.__duplicates = dict()
        set_of_tuples = set(self.__tuples)

        for el in set_of_tuples:
            count = self.__tuples.count(el)
            if(count >1):
                ## get the indices of all occurrences:
                indices = [i for i in range(len(self.__sequ)) if self.__sequ.startswith(el,i)]
                self.__duplicates[el] = indices
        #        print("the following tuple appears more than once:")
        #        print(el)
    #            self.__duplicates[el]=count;

        return self.__duplicates
    def ObtainDictOfRevComps(self):
        dict_of_revcomp_tuples=dict()
        if not self.__tuples:
            print("list of tuples has not yet been created")
            print("please call the method GetListOfTuples(tuple_length) first")
            return None
        else:
            set_of_tuples= set(self.__tuples)
            for el in set_of_tuples:
                rev_comp = dna_sequence.DNASequRevComplement(el)
                if(rev_comp in set_of_tuples):
                    dict_of_revcomp_tuples[el] = rev_comp
        return dict_of_revcomp_tuples

if __name__ == "__main__":
    testsequ  = "ACTGCAACTGACTCAGAGACCCGACTACCGTA"
    sa = SequenceAnalyzer(testsequ)
    lc = sa.CountLetters()
    cg_content = sa.GetCGContent()
    print("sequence: ")
    print(testsequ)
    print("letter count: ")
    print(lc)
    print("cg-content:")
    print(cg_content)
    lot=sa.GetListOfTuples(4)
    contains_duplicates = sa.ContainsDuplicateTuples()
    if(contains_duplicates):
        print("the sequence contains duplicate tuples and thus does not fulfill the DB-property")
    occ = sa.GetDictOfDuplicates()
    print(occ)
    dorc = sa.ObtainDictOfRevComps()
    if(dorc):
        print(dorc)
