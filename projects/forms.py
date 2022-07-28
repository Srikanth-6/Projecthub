from cProfile import label
from matplotlib import widgets
from django.forms import ModelForm
from .models import Projects,Review
from django import forms


class ProjectsForm(ModelForm):
    class Meta:
        model= Projects
        fields=['title','descrption','demo_link','featured_images','source_link','tags']
        widgets={
            'tags':forms.CheckboxSelectMultiple(),
        }

    def __init__(self, *args, **kwargs):
        super(ProjectsForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})

class ReviewForm(ModelForm):
    class Meta:
        model=Review
        fields=['value','body']
        labels={
            'value':'Place your vote here',
            'body':'Add a comment with a vote'
        }

    def __init__(self, *args, **kwargs):
        super(ReviewForm, self).__init__(*args, **kwargs)

        for name, field in self.fields.items():
            field.widget.attrs.update({'class': 'input'})