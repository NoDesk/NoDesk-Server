from django.shortcuts import render
from django.http import HttpResponse
from django.template import RequestContext, loader

from nodesk_chat.models import Post

def index(request):
    latest_messages = Post.objects.order_by('date')
    context = {'latest_messages': latest_messages}
    return render(request, 'index.html', context)
