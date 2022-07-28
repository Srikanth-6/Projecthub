from cProfile import label
from django.forms import ModelForm
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from users.models import Profile,Skill,Message

class CustomUserCreationForm(UserCreationForm):
    
    class Meta:
        model = User
        fields = ('first_name','email','username','password1','password2')
        labels={
            'first_name': 'Name',
        }

class ProfileForm(ModelForm):
    class Meta:
        model=Profile
        fields=['name','email','user_name',
                'location','bio','short_intro','profile_image',
                'social_github','social_twitter','social_website']

class SkillForm(ModelForm):
    class Meta:
        model=Skill
        fields=['name','description']


class MessageForm(ModelForm):
    class Meta:
        model=Message
        fields=['name','email','subject','body']

    def __init__(self, *args, **kwargs):
        super(MessageForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})
