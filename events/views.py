from django.shortcuts import render, redirect
from .utils import read_json, write_json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import login as auth_login, authenticate, logout
# Create your views here.

def register(request):
    if request.method == 'POST':
        uname = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        confirm_password = request.POST['c_password']

        if password != confirm_password:
            messages.error(request, "Password and confirm password do not match")
            return redirect('register')
        
        if User.objects.filter(username=uname).exists():
            messages.error(request, "Username already taken, try another.")
            return redirect('register')

        # Checking if email already exists
        if User.objects.filter(email=email).exists():
            messages.error(request, "Entered Email is already associated with other account, try another")
            return redirect('register')

        else:
            myuser = User.objects.create_user(uname, email, password)
            myuser.save()

            user = authenticate(request, username=uname, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect("/")
            else:
                # Handle the case when authentication fails
                messages.error(request, "Registration successful, but failed to log in. Please try logging in manually.")
                return redirect('login')

    return render(request, "register.html")


def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = User.objects.get(email=email)

        except User.DoesNotExist:
            messages.error(request, "Email not found")
            return redirect('login')
        
        user = authenticate(request, username=user.username, password=password)

        if user is not None:
            auth_login(request, user)
            messages.success(request, "Login successfull!")
            return redirect('/')
        else:
            messages.error(request, "Invalid login credentials")
            return redirect('login')
    return render(request, 'login.html')

def Logout(request):
    logout(request)
    return redirect('/')

def eventList(request):
    events = read_json()
    return render(request, 'events.html', {'events': events})

@login_required(login_url='login')
def event_add(request):
    if request.method == 'POST':
        events = read_json()
        add_event = {
            'id': len(events)+1,
            'title': request.POST['title'],
            'description': request.POST['description'],
            'total_participants': request.POST['total_participants'],
            'start_date': request.POST['start_date'],
            'end_date': request.POST['end_date'],
        }
        events.append(add_event)
        write_json(events)
        messages.success(request, 'Event added successfully!')
        return redirect('events')
    return render(request, 'add_event.html')

def event_update(request, event_id):
    events = read_json()
    event = next((e for e in events if e['id'] == event_id), None)
    if not event:
        return redirect('events')
    
    if request.method == 'POST':
        event['title'] = request.POST['title']
        event['description'] = request.POST['description']
        event['total_participants'] = request.POST['total_participants']
        event['start_date'] = request.POST['start_date']
        event['end_date'] = request.POST['end_date']
        write_json(events)
        messages.success(request, 'Event updated successfully!')
        return redirect('events')
    return render(request, 'update_event.html', {'event': event})

def delete_event(request, event_id):
    events = read_json()
    events = [e for e in events if e['id'] != event_id]
    write_json(events)
    messages.success(request, 'Event deleted successfully!')
    return redirect('events')