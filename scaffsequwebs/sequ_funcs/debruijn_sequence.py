if __name__ == "__main__":
	from debruijn_graph import CDeBruijnGraph
	from dna_sequence import CDNASequence
	from dna_sequence import DNASequRevComplement
else:
	from .debruijn_graph import CDeBruijnGraph
	from .dna_sequence import CDNASequence
	from .dna_sequence import DNASequRevComplement
import numpy as np
import datetime
import random
import sys, threading

class CDeBruijnSequence(CDNASequence):
	def __init__(self,order_sequ=7,rev_comp_free=False,initial_sequence="",length=7560):
		CDNASequence.__init__(self)
		self._sequ=""
		self._order_of_sequ = order_sequ
		self._db_graph = CDeBruijnGraph(self._order_of_sequ-1) ## order of the underlying De Bruijn-Graph is smaller by 1 than the order of the De Bruijn sequence
		self._is_circular = False ##is_circular
		self._rev_comp_free = rev_comp_free
		self._initial_sequence = initial_sequence
		self._scaffold_length = length

		self._solution_found = False
		self._end_reached = False

		self._initial_depth=0
		self._timedelta_max = datetime.timedelta(0,10,0) ## a maximum of 3 s

	#def RemoveSequence(self):
	#	for i in range(0,self._)
	def PreventSequence(self,substring):
		self._db_graph.PreventSequence(substring)
	def PrintEdges(self):
		self._db_graph.PrintEdges()
	def PrintInfo(self):
		print("order of the sequence: ");
		print(self._order_of_sequ);
		print("circularity: ")
		print(self._is_circular)
		print("final scaffold length: ")
		print(self._scaffold_length)
		print("initial sequence: ")
		print(self._initial_sequence)
		## call print-method for underlying De-Bruijn-Graph:
		self._db_graph.PrintInfo();
	def CreateDeBruijnSequence(self):
		## start with random index:
		num_vertices = self._db_graph.GetNumberOfVertices()
		cti = np.random.randint(0,num_vertices)

		if(self._initial_sequence==""):
			#print("initial sequence is empty")
			self._initial_tuple_index = cti
			self._initial_depth=0
		elif(self._initial_sequence!=""):
			#print("initial sequence is not empty")
			first_tuple_string = self._initial_sequence[0:self._db_graph.GetOrder()]
			self._initial_tuple_index=self._db_graph.VertexIndexByName(first_tuple_string)
			self._sequ=self._initial_sequence[0:len(self._initial_sequence)-self._db_graph.GetOrder()]
			self._sequ_last_tuple = self._initial_sequence[len(self._initial_sequence)-self._db_graph.GetOrder():len(self._initial_sequence)]
			cti = self._db_graph.VertexIndexByName(self._sequ_last_tuple)
			self._initial_depth=len(self._sequ)
			self._ConsiderInitialSequence()

		self._starting_time = datetime.datetime.now()
		self.__CreateDeBruijnSequenceRecursively(self._sequ,cti,self._initial_depth,self._rev_comp_free)
	def _ConsiderInitialSequence(self):
		self._RemoveSubsequencesInString(self._initial_sequence)
		if(self._rev_comp_free==True):
			self._RemoveSubsequencesInString(DNASequRevComplement(self._initial_sequence))
	def _RemoveSubsequencesInString(self,string):
		str_length = len(string)
		if(str_length<self._db_graph.GetOrder()+1):
			return
		else:
			subsequences=list()
			for i in range(0,(str_length-self._db_graph.GetOrder())):
				subsequences.append(string[i:i+self._db_graph.GetOrder()+1])
			for cs in subsequences:
				self._db_graph.DeleteEdgesByStrings(cs[0:self._db_graph.GetOrder()],cs[1:self._db_graph.GetOrder()+1])

	def __CreateDeBruijnSequenceRecursively(self,curr_sequ,curr_tuple_index,curr_depth,rev_comp_free):
		self._curr_time = datetime.datetime.now()
		#print(curr_depth)
		if((self._curr_time-self._starting_time)>self._timedelta_max):
			#print("TIME OUT")
			self._end_reached=True
			self._solution_found=False
			return
		if(curr_depth==self._scaffold_length):
			#print("final depth reached")
			#print("time required: ")
			dt = self._curr_time-self._starting_time
			print(dt)
			self._sequ=curr_sequ
			self._end_reached=True
			if(self._is_circular==True):
				if(curr_tuple_index==self._initial_tuple_index):
					#print("circular solution found")
					self._solution_found=True
				else:
					#print("no circular solution found")
					self._solution_found=False
			else:
				#print("linear solution found")
				self._solution_found=True
			return
		else:	## final length not yet reached
			if(self._end_reached==False): ## check whether time-out has occured
				curr_sequ+=self._db_graph.VertexNameByIndex(curr_tuple_index)[0]
				curr_neighbors = self._db_graph.GetNeighborsByVertexIndex(curr_tuple_index)
				num_neighbors = len(curr_neighbors)
				random.shuffle(curr_neighbors)
				#curr_neighbors2 = self._db_graph.GetNeighborsByVertexIndex(curr_tuple_index)
				for i in range(0,num_neighbors):
					rev_comp_removed = False
					first_element = curr_neighbors[0]
					#print(first_element)
					index_rev_comp_first=0
					index_rev_comp_second=0
					contained_tuple=False
					if(rev_comp_free==True):
						#print("curr_")
						curr_tup_sequence = self._db_graph.VertexNameByIndex(curr_tuple_index)[0] + self._db_graph.VertexNameByIndex(first_element)[0:self._db_graph.GetOrder()+1]
						curr_rev_complement = DNASequRevComplement(curr_tup_sequence)
						first_partstring = curr_rev_complement[0:self._db_graph.GetOrder()]
						second_partstring = curr_rev_complement[1:self._db_graph.GetOrder()+1]

						if(self._db_graph.HasConnectionByStrings(curr_rev_complement[0:self._db_graph.GetOrder()],curr_rev_complement[1:self._db_graph.GetOrder()+1])):
							self._db_graph.DeleteEdgesByStrings(curr_rev_complement[0:self._db_graph.GetOrder()],curr_rev_complement[1:self._db_graph.GetOrder()+1])
							rev_comp_removed=True

					## remove current element from list....
					## BASICALLY UNTESTED CODE !
					was_in_list=first_element in curr_neighbors
					if(was_in_list):
						curr_neighbors.remove(first_element)


					self.__CreateDeBruijnSequenceRecursively(curr_sequ,first_element,curr_depth+1,rev_comp_free)

					## BASICALLY UNTESTED CODE
					if(was_in_list):
						curr_neighbors.append(first_element)

					if(rev_comp_removed==True):
						self._db_graph.AppendEdgeByStrings(curr_rev_complement[0:self._db_graph.GetOrder()],curr_rev_complement[1:self._db_graph.GetOrder()+1])



if __name__ == "__main__":

		### super annoying workaround due to recursion limit (or much more stack size limit....)
		### better long-term solution is to change the algorithm from a recursive one to an iterative one....

		order_of_sequ = 7
		rev_comp_free = False
		length = 7560
		def test():
			global order_of_sequ
			global rev_comp_free
			global length
			dbs = CDeBruijnSequence(order_sequ=order_of_sequ,initial_sequence="",length=length,rev_comp_free=rev_comp_free)
			dbs.PrintEdges()
			dbs.PreventSequence("ACTGACTGACTG")
			dbs.PreventSequence("CCCC")

			dbs.CreateDeBruijnSequence()
			sequ = dbs.GetSequence()
			print(sequ)

		sys.setrecursionlimit(20000000)
		threading.stack_size(64000000)
		thread=threading.Thread(target=test)
		thread.start()
		thread.join()

#dbs = CDeBruijnSequence(order_sequ=5,initial_sequence="",length=20,rev_comp_free=True)
#dbs.PrintInfo();
##dbs.PreventSequence("AAAAAA")
#dbs.PreventSequence("CCCCCC")
#dbs.PreventSequence("GGGGGG")
#dbs.PreventSequence("TTTTTT")

#dbs.CreateDeBruijnSequence()
#dbsa = CSequAnalyzer()

#dbstr = dbs.GetSequence()

#print("string:")
#print(dbstr)
