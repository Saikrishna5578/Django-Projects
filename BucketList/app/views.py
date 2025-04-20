from django.shortcuts import redirect, render
from .forms import Registration
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from .models import BucketList
# Create your views here.
def register(request):
    form = Registration()
    if request.method == 'POST':
        form = Registration(request.POST)
        if form.is_valid():
            form.save()
            print("registered")
            return redirect('login')
    return render(request,'register.html',{'form':form})

def log_in(request):
    msg = {}
    if request.method == 'POST':
        usern = request.POST.get('username')
        pswd = request.POST.get('password')
        # print(usern, pswd)
        user = authenticate(request, username = usern, password = pswd)
        # print(user)
        if user is not None:
            login(request,user)
            return redirect('home')
        else:
            msg["cred"] = "Invalild Credentials Please check once again OR CREATE AN ACCOUTN if accoout not exist"
    return render(request, 'login.html', {'msg':msg}) 

def log_out(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
def home(request):
    msg = {}
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('description')
        print(title, desc)
        if title != "":
            BucketList.objects.create(title=title,description=desc,user_id = request.user.id)
            msg['success'] = "CONGRATULATIONS! You have sccussfully added the list item"
            return redirect('list')
        else:
            # print("empty")
            msg['empty'] = "Please Enter the List items"
        
    return render(request, 'index.html',{'msg':msg})

def list(request):
    list = BucketList.objects.filter(user_id = f"{request.user.id}") 
    return render(request, 'list.html', {'list':list})

def history(request):
    list = BucketList.objects.filter(user_id = f"{request.user.id}") 
    return render(request,'history.html', {'list':list})

def edit(request,p):
    list = BucketList.objects.get(id=p)
    if request.method == 'POST':
        title = request.POST.get('title')
        desc = request.POST.get('description')
        list.title, list.description = title, desc
        list.save()
        return redirect('list')
    details = {
        'list':list
    }
    return render(request, 'edit.html',details)

def task(request,id):
    data = BucketList.objects.get(id=id)
    data.completed = True
    data.save()
    
    return redirect('history')

def notask(request,id):
    data = BucketList.objects.get(id=id)
    data.completed = False
    data.save()
    return redirect('list')

def delete(request,id):
    data = BucketList.objects.get(id=id)
    data.delete()
    return redirect('list')