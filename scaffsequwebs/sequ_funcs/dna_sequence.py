import random
import numpy as np
from abc import ABCMeta
#from sequ_analyzer import CSequAnalyzer

DNA_letters = ['A','C','G','T']
## little helper function,
prob_letters = {'A':0.15,'C':0.3,'G':0.3,'T':0.25}
comp_dict = {'A':'T','C':'G','G':'C','T':'A'}

def DNASequComplement(sequ):
	list_comp = list()
	for i in sequ:
		list_comp.append(comp_dict[i])
	return "".join(list_comp)

def DNASequRevComplement(sequ):
	rev = sequ[::-1]
	return DNASequComplement(rev)

def GetLetterWithProb(probs):
	if(np.sum(probs)!=1.0):
		print("probabilities have to sum to 1")
	accum_prob = 0.0
	prob = np.random.random()

	for i in range(0,len(DNA_letters)):
		accum_prob+=probs[i]
		if(accum_prob>=prob):
			return DNA_letters[i]
#def GetKeyWithValueProb(prob_dict):

def TestLetterProb():
	letter_probs = (0.1,0.1,0.2,0.6)
	all_letters = list()
	for i in range(0,1000):
		all_letters.append(GetLetterWithProb(letter_probs))
	return "".join(all_letters)


class CDNASequence(object):
	'''super class for all DNA-Sequence-classes
	contains basic functionality, like reversing and
	complementing sequences'''
	def __init__(self):
		self._sequ=""
		self.__length__=0
		##super(CDNASequence,self).super()
		object.__init__(self)
	def SetSequence(self,sequ):
		self._sequ=sequ
		self.__length__=len(self._sequ)
	def GetSequence(self):
		return self._sequ
	def GetComplement(self):
		return DNASequComplement(self._sequ)
	def GetReverse(self):
		return self._sequ[::-1]
	def GetReverseComplement(self):
		return	DNASequComplement(self.GetReverse())
	def SetOutputPath(self,path):
		''' used for writing/reading sequences to/from files. It
		sets the path for the file.'''
		self.__path__ = path
	def WriteSequenceToFile(self,filename):
		self.__filename__=filename
		self.__comp_path__ = self.__path__ + self.__filename__
		with open(self.__comp_path__,"w") as text_file:
			text_file.write(self._sequ)

class CDNATupleSequence(CDNASequence):
	' the base-class for tuple-based DNA sequences'
	def __init__(self,depth):
		print("entered CDNATupleSequence")
		self.__max_depth=depth
		self.tuples=list()
		#super(CDNASequence,self).__init__()
		CDNASequence.__init__(self)
		print("exit CDNATupleSequence")
	def InitTuples(self):
		self.tuples=list()
		self.__CreateTuples(0,"")
	def __CreateTuples(self,depth,temp):
		if(depth==self.__max_depth):
			self.tuples.append(temp)
		else:
			for i in range(0,len(DNA_letters)):
				self.__CreateTuples(depth+1,temp+(DNA_letters[i]))
	def CreateTupleSequence(self):
		' concatenates the tuples to create a scaffold-sequence'
		random.shuffle(self.tuples)
		for i in range(0,len(self.tuples)):
			self._sequ+=self.tuples[i]
	def DeleteSubsequ(self,subsequ):
		if(len(subsequ)>self.__max_depth):
			print("not possible, length of the subsequence must not exceed the tuple length")
		else:
			tuples_to_delete=list()
			for i in range(0,len(self.tuples)):
				if(subsequ in self.tuples[i]):
					tuples_to_delete.append(self.tuples[i])
			for i in tuples_to_delete:
				self.tuples.remove(i)
	def DeleteTuplesWithLetterAtIndex(self,letter_index,letter):
		tuples_to_delete=list()
		for i in range(0,len(self.tuples)):
			if(self.tuples[i][letter_index]==letter):
				tuples_to_delete.append(self.tuples[i])
		for i in tuples_to_delete:
			self.tuples.remove(i)

class CDNARepTupleSequence(CDNATupleSequence):
	'class for tuple-based sequences with repetitive patterns (e.g. "2A")'
	def __init__(self,depth,rep_pattern):
		#CDNASequence.__init__(self)
		#CDNATupleSequence.__init__(self,depth)
		#super(CDNARepTupleSequence,self).__init__(depth)
		#self.__max_depth = depth
	#	self.tuples=list()
		CDNASequence.__init__(self)
		CDNATupleSequence.__init__(self,depth)
		self.__rep_pattern = rep_pattern
	def CreateRepTupleSequence(self):
		## call init tuples-function....
		#print(self._sequ)
		#print(self.__max_depth)
		#self.InitTuples()
		random.shuffle(self.tuples)
		for i in range(0,len(self.tuples)):
			self._sequ+=self.tuples[i]+self.__rep_pattern

	#def DeleteTupleWithLetterAtIndex(self,letter_index,letter):
	#	tuples_to_delete=list()
	#	for i in range(0,len(self.tuples)):
	#		if(self.tuples[i][letter_index]==letter):
	#			tuples_to_delete.append(self.tuples[i])
#		for i in tuples_to_delete:#
	#		self.tuples.remove(i)

class CDNASequRandom(CDNASequence):
	'class for generating simple random DNA sequences'
	def __init__(self):
		super(CDNASequRandom,self).__init__()
	def CreateRandomSequence(self,length):
		'''creates a random DNA sequence,
		the probability of each letter being 0.25'''
		self.__length__ = length
		self._sequ = ""
		for i in range(0,self.__length__):
			self._sequ+=random.choice(DNA_letters)
	def CreateRandomSequenceWithProbs(self,length,probs):
		'''creates a random DNA sequence,
		with the probability of each letter given by
		probs'''
		self.__length__=length
		for i in range(0,self.__length__):
			self._sequ+=GetLetterWithProb(probs)

if __name__ == "__main__":
		## first: test the basic functionality of
		## the DNA-sequence class:
		sequ1 = "ACTGCAACTGACTCAGAGACCCGACTACCGTA"
		dna_sequ = CDNASequence()
		dna_sequ.SetSequence(sequ1)
		sequ1_rev = dna_sequ.GetReverse()
		sequ1_rev_comp = dna_sequ.GetReverseComplement()

		print("the original sequence was:")
		print(sequ1)
		print("the reversed sequence is:")
		print(sequ1_rev)
		print("the reversed complement is:")
		print(sequ1_rev_comp)

		dna_sequ_reptuple = CDNARepTupleSequence(6,"AA")
		dna_sequ_reptuple.InitTuples()
		dna_sequ_reptuple.CreateRepTupleSequence()
		sequ_reptuple = dna_sequ_reptuple.GetSequence()
		print("repetitive tuple sequence:")
		print(sequ_reptuple)


#tuple_sequence = CDNATupleSequence(4)
#tuple_sequence.DeleteSubsequ("ACAG")
#tuple_sequence.InitTuples()
#tuple_sequence.CreateTupleSequence()
#
#ts = tuple_sequence.GetSequence()
#print(ts)

#tuple_sequence = CDNARepTupleSequence(5,"AA")
#tuple_sequence.InitTuples()
#tuple_sequence.DeleteTuplesWithLetterAtIndex(0,"A")
#tuple_sequence.DeleteTuplesWithLetterAtIndex(4,"A")
#tuple_sequence.DeleteSubsequ("AA")
#tuple_sequence.CreateRepTupleSequence()

#seq = tuple_sequence.GetSequence()
#print(seq)

#random_sequ = CDNASequRandom()
#random_sequ.CreateRandomSequence(20)
#sequ = random_sequ.GetSequence()

#print("original sequence:")
#print(sequ)
#
#print("complementary sequence:")
#print(random_sequ.GetComplement())
#print("reverse: ")
#print(random_sequ.GetReverse())
#print("reverse complement: ")
#print(random_sequ.GetReverseComplement())
#test = TestLetterProb()
#print(test)
##sequan = SequAnalyzer(test)
#squan.Analyze()
#
## create tuple - sequence
