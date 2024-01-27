from django.shortcuts import render,redirect
from django.contrib import messages
from django.contrib.auth.models import User, auth
from .models import Todo
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
def index(request):
    if request.method == 'POST':
        task_item = request.POST['task_item']
        new_todo = Todo(user=request.user, item=task_item)
        new_todo.save()

    todo_items = Todo.objects.filter(user=request.user)
    todo_numb = len(todo_items)

    numoftrue = Todo.objects.filter(user=request.user, status=True).count()

    remaining = todo_numb-numoftrue
    
    contex = {
        'todo_items': todo_items,
        'todo_numb':todo_numb,
        'numoftrue':numoftrue,
        'remaining':remaining,
    }

    return render(request, 'index.html',contex)


def signup(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        password2 = request.POST['password2']

        if password == password2:
            if User.objects.filter(email=email).exists():
                messages.info(request,'email already in use')
                return redirect('signup')
            elif User.objects.filter(username=username).exists():
                messages.info(request, 'username already in use')
                return redirect('signup')
            elif len(password)<3:
                messages.info(request, "password is too short")
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                return redirect('login')
        else:
            messages.info(request, 'password not thesame')
            return redirect('register')

    else:
        return render(request, 'signup.html')
    


def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']

        user = auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('index')
        else:
            messages.info(request, 'Invalid credentials try signing up')
            return redirect('login')
    
    else:
        return render (request, 'login.html')
    

def logout_todo(request):
    auth.logout(request)
    return redirect('login')

def DeleteTask(request, id):
    get_todo = Todo.objects.get(user=request.user, id=id)
    get_todo.delete()

    return redirect('index')

def DeleteAllTask(request):
    dele = Todo.objects.filter(user=request.user)
    dele.delete()

    return redirect('index')

def Update(request, id):
    update_todo = Todo.objects.get(user=request.user, id=id)
    update_todo.status = True
    update_todo.save()

    return redirect('index')

