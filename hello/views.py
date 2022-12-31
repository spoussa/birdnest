from django.shortcuts import render
from hello.models import Owner
import get

# Create your views here.
from django.http import HttpResponse

def home(request):
    #vios = get.violators()
    db =  Owner.objects.all()
    return render(request,"home.html",{"items" : db})