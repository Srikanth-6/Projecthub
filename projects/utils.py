from django.db.models import Q 
from .models import Projects,Tag
from django.core.paginator import Paginator,PageNotAnInteger,EmptyPage

def paginateProjects(request,project,results):
    page=request.GET.get('page')
    paginator=Paginator(project, results)
    try:
        project=paginator.page(page)
    except PageNotAnInteger:
        page=1
        project=paginator.page(page)
    except EmptyPage:
        page=paginator.num_pages
        project=paginator.page(page)
    left_index=(int (page)-1)
    if left_index<1:
        left_index=1
    right_index=(int(page)+2)
    if right_index>paginator.num_pages:
        right_index=paginator.num_pages+1
    custom_range=range(left_index,right_index)
    return custom_range,project

def searchProjects(request):
    search_query=''
    if request.GET.get('search_query'):
        search_query=request.GET.get('search_query')
    tags=Tag.objects.filter(name__icontains=search_query)
    project=Projects.objects.distinct().filter(
                                    Q(title__icontains=search_query) |
                                    Q(descrption__icontains=search_query) |
                                    Q(owner__name__icontains=search_query) |
                                    Q(tags__in=tags)
                                    )
    return project,search_query