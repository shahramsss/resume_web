from django.shortcuts import render
from django.views import View


class HomeView(View):
    def get(self , request):
        return render(request,"home/home.html")

class SkillsView(View):
    def get(self , request):
        return render(request,"home/skills.html")