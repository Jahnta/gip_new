from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def overview(request):
    return render(request, 'main/overview.html')
