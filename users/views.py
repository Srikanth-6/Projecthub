from datetime import datetime
from pickle import FALSE
from django.shortcuts import render,redirect
from django.contrib.auth import login,authenticate,logout
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required

from .forms import CustomUserCreationForm, ProfileForm, SkillForm,MessageForm
from django.contrib import messages
from matplotlib.style import context
from .utils import searchProfiles,paginateProfiles
from .models import Profile

# Create your views here.


def loginUser(request):
    page='login'
    context={'page':page}
    if request.user.is_authenticated:
        return redirect('profiles')

    if request.method=="POST":
        username=request.POST['username'].lower()
        password=request.POST['password']
        try:
            user=User.objects.get(username=username)
        except:
            messages.error(request,"Username does'nt exist")
        
        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            return redirect(request.GET['next'] if 'next' in request.GET else 'profiles')
        else:
            messages.error(request,'Username or password are incorrect')
    return render(request,'users/login_register.html',context)


def registerUser(request):
    page='register'
    form =CustomUserCreationForm()
    if request.method=="POST":
        form=CustomUserCreationForm(request.POST)
        if form.is_valid():
            user=form.save(commit=False)
            user.username=user.username.lower()
            user.save()
            messages.success(request,'the user is created succesfully!')
            login(request,user)
            return redirect('edit-account')
        else:
            messages.success(request,'An error has occured during registration.')
    context={'page':page,'form': form}
    return render(request,'users/login_register.html',context)

def logoutUser(request):
    logout(request)
    messages.info(request,'User was logged out!!!')
    return redirect('login')


def profile(request):
    profile,search_query=searchProfiles(request)
    custom_range,profile=paginateProfiles(request,profile,3)
    context={'profiles':profile,'search_query': search_query,'custom_range':custom_range}
    return render(request,'users/profile.html',context)

def userProfile(request,pk):
    profilex=Profile.objects.get(id=pk)
    topskills=profilex.skill_set.exclude(description__exact="")
    otherskills=profilex.skill_set.filter(description="")
    context={'profilex':profilex,"topskills": topskills,"otherskills":otherskills}
    return render(request,'users/user-profile.html',context)


@login_required(login_url='login')
def userAccount(request):
    profile=request.user.profile
    skills=profile.skill_set.all()
    projects=profile.projects_set.all()
    context={'profile': profile,'skills': skills,'projects':projects}
    return render(request,'users/account.html',context)

@login_required(login_url='login')
def editAccount(request):
    profile=request.user.profile
    form=ProfileForm(instance=profile)
    if request.method=='POST':
        form=ProfileForm(request.POST,request.FILES,instance=profile)
        form.save()
        return redirect('account')
    context={'form':form}
    return render(request,'users/profile_form.html',context)

@login_required(login_url='login')
def createSkill(request):
    profile=request.user.profile
    form=SkillForm()
    if request.method=="POST":
        form=SkillForm(request.POST)
        if form.is_valid():
            skill=form.save(commit=False)
            skill.owner=profile
            skill.save()
            messages.success(request,'Skill was added succesfully!!')
            return redirect('account')
    context={'form': form}
    return render(request,'users/skill_form.html',context)

@login_required(login_url='login')
def updateSkill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    form=SkillForm(instance=skill)
    if request.method=="POST":
        form=SkillForm(request.POST,instance=skill)
        if form.is_valid():
            skill.save()
            messages.success(request,'Skill was updated succesfully!!')
            return redirect('account')
    context={'form': form}
    return render(request,'users/skill_form.html',context)


@login_required(login_url='login')
def deleteSkill(request,pk):
    profile=request.user.profile
    skill=profile.skill_set.get(id=pk)
    if request.method=="POST":
        skill.delete()
        messages.success(request,'Skill was deleted succesfully!!')
        return redirect('account')
    context={'object':skill}
    return render(request,'delete.html',context)


@login_required(login_url='login')
def inbox(request):
    profile=request.user.profile
    messageRequests=profile.messages.all()
    unreadCount=messageRequests.filter(isread=False).count()
    context={'messageRequests':messageRequests,'unreadCount':unreadCount}
    return render(request,'users/inbox.html',context)


@login_required(login_url='login')
def readmessage(request,pk):
    profile=request.user.profile
    message=profile.messages.get(id=pk)
    if message.isread==False:
        message.isread=True
        message.save()
    context={'message':message}
    return render(request,'users/message.html',context)

def createMessage(request,pk):
    recipient=Profile.objects.get(id=pk)
    form=MessageForm()
    context={'recipient':recipient,'form':form}
    sender=None
    if request.user.is_authenticated:
        sender=request.user.profile
    if request.method=='POST':
        form=MessageForm(request.POST)
        if form.is_valid():
            message=form.save(commit=False)
            message.recipient=recipient
            message.sender=sender
            if sender:
                message.name=sender.name
                message.email=sender.email
            message.save()
            messages.success(request,"Your message is sent successfully!!!")
            return redirect('user-profile',pk=recipient.id)
    return render(request,'users/message_form.html',context)
