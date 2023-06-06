from msilib.schema import File
from multiprocessing import AuthenticationError
import os
from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login
from django.http import Http404, HttpResponse
from django_project import settings
from blog.models import FilesAdmin
from django.contrib.auth.forms import AuthenticationForm

def register(request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            login(request, user)
            return redirect('home.html')
        else:
            form = UserCreationForm()
            return render(request, 'blog/register.html', {'form': form})
# def login(request):
#     if request.method == 'POST':
#         form = AuthenticationError(request, data=request.POST)
#         if form.is_valid():
#             username = form.cleaned_data.get('username')
#             password = form.cleaned_data.get('password')
#             user = authenticate(username=username, password=password)
#             if user is not None:
#                 login(request, user)
#                 return redirect('home')
#             else:
#                 form.add_error(None, "Invalid username or password.")
#     else:
#         form = AuthenticationForm()
#         return render(request, 'login.html', {'form': form})
def search(request):
    query = request.GET.get('query')
    results = FilesAdmin.objects.filter(title__icontains=query)
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'blog/templates/blog/search.html', context)
def home(request):
    context={'file':FilesAdmin.objects.all()}
    return render(request,'blog/home.html',context)

def download(request,path):
    file_path=os.path.join(settings.MEDIA_ROOT,path)
    if os.path.exists(file_path):
        with open(file_path,'rb')as fh:
            response=HttpResponse(fh.read(),content_type="application/adminupload")
            response['Content-Disposition']='inline;filename='+os.path.basename(file_path)
            return response  
    raise Http404