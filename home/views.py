from django.shortcuts import render, get_list_or_404
from django.views import View
from .models import Project, ProjectImage


class HomeView(View):
    def get(self, request):
        projects = Project.objects.all()[:3]
        return render(request, "home/home.html",{'projects':projects})


class SkillsView(View):
    def get(self, request):
        return render(request, "home/skills.html")


class AboutView(View):
    def get(self, request):
        return render(request, "home/about.html")


class ContactView(View):
    def get(self, request):
        return render(request, "home/contact.html")


class ProjectsView(View):
    def get(self, request):
        projects = Project.objects.all()
        return render(request, "home/projects.html", {"projects": projects})


class ProjectDetailView(View):
    pass
    # def get(self , request):
    #     return render(request,"home/contact.html")
