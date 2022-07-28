from email.policy import default
from enum import unique
from pyexpat import model
from tkinter import CASCADE
from django.db import models
import uuid
from users.models import Profile
from users.views import profile

# Create your models here.
class Projects(models.Model):
    owner=models.ForeignKey(Profile,null=True,blank=True,on_delete=models.CASCADE)
    title=models.CharField(max_length=20)
    descrption=models.TextField(null=True,blank=True)
    demo_link=models.CharField(max_length=2000,null=True,blank=True)
    source_link=models.CharField(max_length=2000,null=True,blank=True)
    featured_images=models.ImageField(null=True,blank=True,default="default.jpg")
    tags=models.ManyToManyField('Tag',blank=True)
    vote_total=models.IntegerField(default=0,null=True,blank=True)
    vote_ratio=models.IntegerField(default=0,null=True,blank=True)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering=['-vote_ratio','-vote_total','title']

    @property
    def ImageURL(self):
        url=''
        try:
            url=self.featured_images.url
        except:
            url=''
        return url

    @property
    def GetVoteCount(self):
        reviews=self.review_set.all()
        upvotes=reviews.filter(value='up').count()
        total_votes=reviews.count()
        ratio=upvotes/total_votes*100
        self.vote_total=total_votes
        self.vote_ratio=ratio
        
        self.save()
    
    def getreviews(self):
        reviews=self.review_set.all().values_list('owner_id',flat=True)
        return reviews


class Review(models.Model):

    VOTE_TYPE=(
        ('up','Up Vote'),
        ('down','Down Vote'),
    )

    owner=models.ForeignKey(Profile,on_delete=models.CASCADE,null=True)
    project=models.ForeignKey(Projects,on_delete=models.CASCADE)
    body=models.TextField(null=True,blank=True)
    value=models.CharField(max_length=200,choices=VOTE_TYPE)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)

    class Meta:
        unique_together=[['owner','project']]
    
    def __str__(self):
        return self.value


class Tag(models.Model):
    name=models.CharField(max_length=200)
    created=models.DateTimeField(auto_now_add=True)
    id=models.UUIDField(default=uuid.uuid4,unique=True,primary_key=True,editable=False)
    def __str__(self):
        return self.name