from django.shortcuts import render, redirect
from .utils import read_json, write_json
from django.contrib.auth.decorators import login_required
from django.contrib import messages
# Create your views here.

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
        return redirect('event_list')
    return render(request, 'update_event.html', {'event': event})

def delete_event(request, event_id):
    events = read_json()
    events = [e for e in events if e['id'] != event_id]
    write_json(events)
    messages.success(request, 'Event deleted successfully!')
    return redirect('events.html')

def filter_events(request):
    events = read_json()
    title = request.GET.get('title')
    start_date = request.GET.get('start_date')
    end_date = request.GET.get('end_date')

    if title:
        events = [event for event in events if title.lower() in event['title'].lower()]
    if start_date:
        events = [event for event in events if event['start_date'] >= start_date]
    if end_date:
        events = [event for event in events if event['end_date'] <= end_date]

    return render(request, 'events.html', {'events': events})