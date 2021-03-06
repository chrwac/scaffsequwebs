from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from . import forms
from .models import GeneratedSequence

from .models import DeBruijnSequence_DBModel
from .models import RepetitiveSequence_DBModel
from .models import MarkovSequence_DBModel

from .sequ_funcs.markov_sequence import CMarkovSequence
from .sequ_funcs.analyze_sequence import SequenceAnalyzer
from .sequ_funcs.validate_sequence import SequenceValidator
from .sequ_funcs.dna_sequence import  CDNASequence
from .sequ_funcs.dna_sequence import  CDNARepTupleSequence
from .sequ_funcs.debruijn_sequence import CDeBruijnSequence
import sys, threading
import copy

db_sequence=""

class HomeView(TemplateView):
    template_name="main/index.html"
    def get(self,request):
        return render(request,self.template_name)

class DBView(TemplateView):
    template_name="dbsequence/dbsequence.html"
    def get(self,request):
        form = forms.DBSequForm()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form = forms.DBSequForm(request.POST)
        order=7
        init_sequ = ""
        forbidden_sequ=""
        sequence_name=""
        user_name=""
        rev_comp_free = False
        length=7560
        if(form.is_valid()):
            order = form.cleaned_data["order"]
            init_sequ = form.cleaned_data["init_sequ"]
            forbidden_sequ = form.cleaned_data["forbidden_sequ"]
            length = form.cleaned_data["length"]
            rev_comp_free=form.cleaned_data["rev_comp_free"]
            sequence_name = form.cleaned_data["sequence_name"]
            user_name = form.cleaned_data["user_name"]

        if(len(init_sequ)>0):
            sv = SequenceValidator(init_sequ)
            if(sv.IsValid()==False):
                param_dict = {"sequ":init_sequ}
                return render(request,"errors/error_invalid_sequence.html",param_dict)
            else:
                init_sequ = sv.GetSequence()
        ## check the same thing with the sequences that shall be prevented:
        list_of_forbidden_sequs=list()
        if(len(forbidden_sequ)>0):
            print("sequences shall be forbidden:")
            print(forbidden_sequ)
            forbidden_sequ=forbidden_sequ.replace("\r","")
            forbidden_sequ=forbidden_sequ.replace("\t","")
            forbidden_sequ=forbidden_sequ.replace("\n","")
            list_of_sequs = forbidden_sequ.strip().split(";")
            if "" in list_of_sequs:
                list_of_sequs.remove("")
            for i in list_of_sequs:
                sv = SequenceValidator(i)
                if(sv.IsValid()==False):
                    param_dict = {"sequ":i}
                    return render(request,"errors/error_invalid_sequence.html",param_dict)
                else:
                    list_of_forbidden_sequs.append(sv.GetSequence())
            print(list_of_forbidden_sequs)

        def test():
            global db_sequence
            #print(length)
            #print(order)
            dbs = CDeBruijnSequence(order_sequ=order,rev_comp_free=rev_comp_free,initial_sequence=init_sequ,length=length)
            if(list_of_forbidden_sequs):
                for el in list_of_forbidden_sequs:
                    dbs.PreventSequence(el)
            dbs.CreateDeBruijnSequence()
            db_sequence = copy.copy(dbs.GetSequence())
            #print(db_sequence)

        print("SOLUTION: ")
        print(db_sequence)
        sys.setrecursionlimit(20000000)
        threading.stack_size(64000000)
        thread=threading.Thread(target=test)
        thread.start()
        thread.join()

        gs_db = DeBruijnSequence_DBModel(user_name=user_name,sequ_name=sequence_name,db_order=order,sequ_length=len(db_sequence),sequence=db_sequence)
        gs_db.save()

        param_dict = {"debruijn_sequence":db_sequence}
        return render(request,"dbsequence/dbsequence_response.html",param_dict)



class RepSequView(TemplateView):
    template_name="repsequ/repsequ.html"
    def get(self,request):
        form = forms.RepSequForm()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form = forms.RepSequForm(request.POST)
        rep_sequ  = ""
        length_of_variable_part = 0
        sequence_name=""
        user_name=""
        if(form.is_valid()):
            rep_sequ = form.cleaned_data["rep_sequ"]
            length_of_variable_part = form.cleaned_data["length_of_variable_part"]
            sequence_name =  form.cleaned_data["sequence_name"]
            user_name = form.cleaned_data["user_name"]

        dna_sequ_reptuple = CDNARepTupleSequence(length_of_variable_part,rep_sequ)
        dna_sequ_reptuple.InitTuples()
        dna_sequ_reptuple.DeleteSubsequ(rep_sequ)
        dna_sequ_reptuple.DeleteTuplesWithLetterAtIndex(0,rep_sequ[0])
        dna_sequ_reptuple.DeleteTuplesWithLetterAtIndex(length_of_variable_part-1,rep_sequ[0])
        dna_sequ_reptuple.CreateRepTupleSequence()
        sequ_reptuple = dna_sequ_reptuple.GetSequence()

        gs_db = RepetitiveSequence_DBModel(user_name=user_name,sequ_name=sequence_name,length_of_variable_part=length_of_variable_part,sequ_length=len(sequ_reptuple),sequence=sequ_reptuple)
        gs_db.save()

        param_dict = {"rep_sequence":sequ_reptuple}
        return render(request,"repsequ/repsequ_response.html",param_dict)

class MarkSequView(TemplateView):
    template_name="marksequ/marksequ.html"
    def get(self,request):
        form = forms.MarkSequForm()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        #template_name="marksequ/marksequ_response.html"
        form = forms.MarkSequForm(request.POST)
        mark_order=0
        sequ_length=0
        user_name=""
        sequence_name=""

        if(form.is_valid()):
            mark_order = form.cleaned_data["mark_order"]
            sequ_length = form.cleaned_data["sequ_length"]
            train_sequ = form.cleaned_data["train_sequ"]
            sequence_name = form.cleaned_data["sequence_name"]
            user_name = form.cleaned_data["user_name"]

        ## distinguish between two cases:
        ## has a training sequence been given as an input(Y/N):
        ## 1st case: trainng sequence was not given:
        markov_sequ = ""
        if(len(train_sequ)==0):
            ms = CMarkovSequence(mark_order)
            ms.CreateFirstOrderSequence(sequ_length)
            markov_sequ = ms.GetSequence()
            #gs = GeneratedSequence(user_name="Christian",sequence=markov_sequ,sequence_type="markov sequence")
            gs_db = MarkovSequence_DBModel(user_name=user_name,sequ_name=sequence_name,markov_order=1,sequ_length=len(markov_sequ),sequence=markov_sequ)
            gs_db.save()
            return render(request,"marksequ/marksequ_response.html",{'markov_sequence':markov_sequ})

        else:
            sv = SequenceValidator(train_sequ)
            if((sv.IsValid()==False)):
                param_dict = {"sequ":train_sequ}
                return render(request,"errors/error_invalid_sequence.html",param_dict)
            else:
                train_sequ = sv.GetSequence()
                ms = CMarkovSequence(mark_order)
                ms.TrainMarkovModel(train_sequ)
                ms.CreateSequenceFromTrainedModel(sequ_length)
                markov_sequ = ms.GetSequence()

        gs_db = MarkovSequence_DBModel(user_name=user_name,sequ_name=sequence_name,markov_order=mark_order,sequ_length=len(markov_sequ),sequence=markov_sequ)
        gs_db.save()

        return render(request,"marksequ/marksequ_response.html",{'markov_sequence':markov_sequ})

class CheckSequView(TemplateView):
    template_name="checksequ/checksequ.html"
    def get(self,request):
        form = forms.CheckSequForm()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form = forms.CheckSequForm(request.POST)
        sequ=""
        db_order=7
        check_DB_Property = False
        check_RC_free = False

        if(form.is_valid()):
            sequ = form.cleaned_data["sequence"]
            db_order = form.cleaned_data["db_order"]
            check_DB_Property = form.cleaned_data["check_DB_Property"]
            check_RC_free = form.cleaned_data["check_RC_free"]
        ## check whether the sequence is a valid DNA sequence:
        sv = SequenceValidator(sequ)
        if((sv.IsValid()==False) or (len(sequ)==0)):
            param_dict = {"sequ":sequ}
            return render(request,"errors/error_invalid_sequence.html",param_dict)
        else:
            sequ = sv.GetSequence()
            sequ_analyzer = SequenceAnalyzer(sv.GetSequence())
            letter_count = sequ_analyzer.CountLetters()
            cg_content = sequ_analyzer.GetCGContent()
            param_dict = {"sequ":sequ,"letter_count":letter_count,"cg_content":cg_content}
            if(check_DB_Property):
                sequ_analyzer.GetListOfTuples(db_order)
                contains_duplicates = sequ_analyzer.ContainsDuplicateTuples()
                message=""
                if(contains_duplicates):
                    message = "Sequence contains duplicates"
                    dict_of_duplicates = sequ_analyzer.GetDictOfDuplicates()
                    string_of_duplicates = ""
                    for key,value in dict_of_duplicates.items():
                        string_of_duplicates+=key+": ["
                        for el in value:
                            string_of_duplicates+=str(el)+" "
                        string_of_duplicates+="] \n"

                    param_dict["string_of_duplicates"] = string_of_duplicates
                else:
                    message = "Sequence does not contain duplicates"

                param_dict["message"] = message
            if(check_RC_free):
                sequ_analyzer.GetListOfTuples(db_order) ## could have already been called --> room for improvement here..
                dict_of_revcomps = sequ_analyzer.ObtainDictOfRevComps()
                if dict_of_revcomps is not None:
                    if(len(dict_of_revcomps.keys())==0):
                        message_revcomp = "No reverse complementary tuples found"
                    else:
                        message_revcomp = "Reverse complementary tuples were found"
                        string_of_revcomps = ""
                        for key,value in dict_of_revcomps.items():
                            string_of_revcomps+=key + ": " + value + "\n"

                        param_dict["string_of_revcomps"] = string_of_revcomps
                    param_dict["message_revcomp"] = message_revcomp

            return render(request,"checksequ/checksequ_response.html",param_dict)

class RevCompView(TemplateView):
    template_name = "revcomp/revcomp.html"
    def get(self,request):
        form = forms.RevCompForm()
        return render(request,self.template_name,{"form":form})
    def post(self,request):
        form = forms.RevCompForm(request.POST)
        sequ=""
        reverse=False
        complement=False
        if(form.is_valid()):
            sequ = form.cleaned_data["sequence"]
            reverse=form.cleaned_data["reverse"]
            complement=form.cleaned_data["complement"]
        message_string = "reverse: "+ str(reverse) + "complement: "+  str(complement)
        ## CHECK FOR VALIDITY OF THE ENTERED SEQUENCE:
        sv = SequenceValidator(sequ)
        sequ = sv.GetSequence()
        orig_sequ = sequ
        if((sv.IsValid()==False) or (len(sequ)==0)):
            param_dict = {"sequ":sequ}
            return render(request,"errors/error_invalid_sequence.html",param_dict)
        else:
            dna_sequ = CDNASequence()
            dna_sequ.SetSequence(sequ)
            if(reverse==True):
                sequ = dna_sequ.GetReverse()
                dna_sequ.SetSequence(sequ)
            if(complement==True):
                sequ = dna_sequ.GetComplement()

            param_dict = {"orig_sequ":orig_sequ,"sequ":sequ}
            return render(request,"revcomp/revcomp_response.html",param_dict)
