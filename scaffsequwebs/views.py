from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from . import forms
from .models import GeneratedSequence
from .sequ_funcs.create_markov_sequence import MarkovSequence
from .sequ_funcs.analyze_sequence import SequenceAnalyzer
from .sequ_funcs.validate_sequence import SequenceValidator
from .sequ_funcs.dna_sequence import  CDNASequence

class HomeView(TemplateView):
    template_name="main/index.html"
    def get(self,request):
        return render(request,self.template_name)

class DBView(TemplateView):
    template_name="dbsequence/dbsequence.html"
    def get(self,request):
        form = forms.DBSequForm()
        return render(request,self.template_name,{'form':form})

class RepSequView(TemplateView):
    template_name="repsequ/repsequ.html"
    def get(self,request):
        form = forms.RepSequForm()
        return render(request,self.template_name,{'form':form})

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
        if(form.is_valid()):
            mark_order = form.cleaned_data["mark_order"]
            sequ_length = form.cleaned_data["sequ_length"]
        ms = MarkovSequence(mark_order)
        sequ = ms.CreateFirstOrderSequence(sequ_length)
        gs = GeneratedSequence(user_name="Christian",sequence=sequ,sequence_type="markov sequence")
        gs.save()
        return render(request,"marksequ/marksequ_response.html",{'markov_sequence':sequ})

class CheckSequView(TemplateView):
    template_name="checksequ/checksequ.html"
    def get(self,request):
        form = forms.CheckSequForm()
        return render(request,self.template_name,{'form':form})
    def post(self,request):
        form = forms.CheckSequForm(request.POST)
        sequ=""
        if(form.is_valid()):
            sequ = form.cleaned_data["sequence"]
        ## check whether the sequence is a valid DNA sequence:
        sv = SequenceValidator(sequ)
        if((sv.IsValid()==False) or (len(sequ)==0)):
            param_dict = {"sequ":sequ}
            return render(request,"errors/error_invalid_sequence.html",param_dict)
        else:
            sequ_analyzer = SequenceAnalyzer(sv.GetSequence())
            letter_count = sequ_analyzer.CountLetters()
            param_dict = {"letter_count":letter_count}
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
            #pass
