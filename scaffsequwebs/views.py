from django.http import HttpResponse
from django.views.generic import TemplateView
from django.shortcuts import render

def index(request):
    return HttpResponse("<h1> This is the most simple website imaginable </h1>")

class HomeView(TemplateView):
    template_name="main/index.html"
    def get(self,request):
        return render(request,self.template_name)

class DBView(TemplateView):
    template_name="dbsequence/dbsequence.html"
    def get(self,request):
        return render(request,self.template_name)
