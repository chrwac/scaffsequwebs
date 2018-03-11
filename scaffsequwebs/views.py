from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render
from . import forms
from .models import GeneratedSequence
from .create_markov_sequence import MarkovSequence
from .analyze_sequence import SequenceAnalyzer
#def index(request):
#    return HttpResponse("<h1> This is the most simple website imaginable </h1>")

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
        sequ_analyzer = SequenceAnalyzer(sequ)
        letter_count = sequ_analyzer.CountLetters()
        param_dict = {"letter_count":letter_count}
        return render(request,"checksequ/checksequ_response.html",param_dict)
