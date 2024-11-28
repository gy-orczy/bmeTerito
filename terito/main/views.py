from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def main(request):

    if request.method == 'POST':
        form = request.POST

    else:
        return render(request, 'main/main.html', {})
    
