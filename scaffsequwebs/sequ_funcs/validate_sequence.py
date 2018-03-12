"""
Functionality to check, whether a particular
sequence is a valid DNA-sequence
containing only the 4 letters ("A","C","G","T")
"""
DNA_letters = ['A','C','G','T']
## usage of the class:#

## 1. create object of type SequenceValidator
##    sv = SequenceValidator(sequ)
## 2. check validity with IsValid() - method:
##    iv = sv.IsValid()
## 3. return the initial sequence in upper charset
##    sequ = sv.GetSequence()

class SequenceValidator:
    def __init__(self,sequ):
        self.__sequ = sequ.upper()
    def IsValid(self):
        """ IsValid() counts the letters "A","C","G","T"
        and compares the sum of their frequencies to the
        length of the entire sequence"""
        self.__num_DNA_letters = self.__sequ.count("A")+self.__sequ.count("C")+ \
        self.__sequ.count("G")+self.__sequ.count("T")
        if(self.__num_DNA_letters!=len(self.__sequ)):
            return False
        return True
    def GetSequence(self):
        return self.__sequ;

## Test the functionality if script is run directly (not loaded as a module)
if __name__ == "__main__":
    sequ1 = "AcTGgCTaCGccctGA"
    sv = SequenceValidator(sequ1)
    if(sv.IsValid()):
        print(sequ1 + " is valid")
    else:
        print(sequ1 + " is not a valid DNA sequence")
    sequ1 = sv.GetSequence()
    print(sequ1)
    sequ2 = "ACTacGTGGGCTAATTGGCCcta"
    sv = SequenceValidator(sequ2)
    if(sv.IsValid()):
        print(sequ2 + " is valid")
    else:
        print(sequ2 + " is not a valid DNA sequence")
    sequ2 = sv.GetSequence()
    print(sequ2)
