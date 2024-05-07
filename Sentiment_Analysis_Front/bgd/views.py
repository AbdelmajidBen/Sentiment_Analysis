from django.shortcuts import render
# Create your views here.


def say_hello(request):
    return render(request, 'hello.html')

def dashboard(request):
    return render(request, 'dashboard.html')

def architecture(request):
    return render(request, 'architecture.html')
# bgd/views.py


# bgd/views.py
from django.shortcuts import render
from .models import Tweet

#def data(request):
 #   # Query all documents from MongoDB collection
  #  tweets = Tweet.objects.all()[:20] 
   # return render(request, 'data.html', {'tweets': tweets})
from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import Tweet

def data(request):
    tweets_list = Tweet.objects.all()
    tweets_per_page = 20
    paginator = Paginator(tweets_list, tweets_per_page)
    page_number = request.GET.get('page', 1)
    try:
        tweets = paginator.page(page_number)
    except PageNotAnInteger:
        tweets = paginator.page(1)
    except EmptyPage:
        tweets = paginator.page(paginator.num_pages)
    return render(request, 'data.html', {'tweets': tweets})






def testing(request):
    return render(request, 'testing.html')

def models(request):
    return render(request, 'models.html')

def team(request):
    return render(request, 'team.html')

