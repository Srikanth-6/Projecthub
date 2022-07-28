from distutils.log import info
from turtle import right
from unittest import result
from django.shortcuts import render,redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from .models import Projects,Tag
from django.contrib import messages
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage
from .forms import ProjectsForm, ReviewForm
from .utils import paginateProjects, searchProjects
import pandas as pd

def projects(request):
    project,search_query=searchProjects(request)
    custom_range,project=paginateProjects(request,project,6)
    context={"projects":project, 'search_query':search_query,'custom_range':custom_range}
    return render(request,'projects/projects.html',context)

def project(request,pk):
    projectOBJ=Projects.objects.get(id=pk)
    tags=projectOBJ.tags.all()
    form=ReviewForm()
    if request.method=='POST':
        form=ReviewForm(request.POST)
        review=form.save(commit=False)
        review.project=projectOBJ
        review.owner=request.user.profile
        review.save()

        #update votecount
        projectOBJ.GetVoteCount

        messages.success(request,'Review has been submitted succcessully!!')

        return redirect('project',pk=projectOBJ.id)

    return render(request,'projects/single-project.html',{"project": projectOBJ,"tags":tags,'form':form})


@login_required(login_url='login')
def createProject(request):
    profile=request.user.profile
    form=ProjectsForm()
    if request.method=='POST':
        form=ProjectsForm(request.POST,request.FILES)
        if form.is_valid()==True:
            project=form.save()
            project.owner=profile
            project.save()
            return redirect('account')
    context={'form':form}
    return render(request,'projects/Project_form.html',context)


@login_required(login_url='login')
def updateProject(request,pk):
    profile=request.user.profile
    project=profile.projects_set.get(id=pk)
    checktags=project.tags.all()
    print(checktags)
    form=ProjectsForm(instance=project)
    if request.method=='POST':
        newtags=request.POST.get('newtags').split()
        form=ProjectsForm(request.POST,request.FILES,instance=project)
        if form.is_valid()==True:
            project=form.save()
            for tag in newtags:
                tag,created=Tag.objects.get_or_create(name=tag)
                project.tags.add(tag)
            return redirect('account')
    context={'form':form,'project':project}
    print(form['tags'])
    return render(request,'projects/Project_form.html',context)


@login_required(login_url='login')
def deleteProject(request,pk):
    profile=request.user.profile
    project=profile.projects_set.get(id=pk)
    context={'object':project}
    if request.method=='POST':
        project.delete()
        return redirect('account')
    return render(request,'delete.html',context)
