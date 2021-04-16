from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Topic, Entry
from .forms import TopicForm, EntryForm


# Create your views here.

def index(request):
    """Strona główna dla aplikacji Resident Platform."""
    return render(request, 'residents_platform/index.html')



def topics(request):
    """wyświetla wszystkie tematy bez logowania lub rejestracji."""
    topics = Topic.objects.order_by('date_added')
    context = {'topics': topics}
    return render(request, 'residents_platform/topics.html', context)


def topic(request, topic_id):
    """Wyświetla pojedynczy temat i wszystkie wpisy bez logowania lub rejestracji."""
    topic = Topic.objects.get(id=topic_id)
    entries = topic.entry_set.order_by('-date_added')
    context = {'topic': topic, 'entries': entries}
    return render(request, 'residents_platform/topic.html', context)


@login_required
def new_topic(request):
    """Dodaj nowy temat."""
    if request.method != 'POST':
        # Nie przekazano żadnych danych, należy utworzyć pusty formularz.
        form = TopicForm()
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = TopicForm(data=request.POST)
        if form.is_valid():
            new_topic = form.save(commit=False)
            new_topic.owner = request.user
            form.save()
            return redirect('residents_platform:topics')
    # Wyświetlenie pustego formularza.
    context = {'form': form}
    return render(request, 'residents_platform/new_topic.html', context)



@login_required
def new_entry(request, topic_id):
    """Dodanie nowego wpisu dla określonego tematu."""
    topic = Topic.objects.get(id=topic_id)

    if request.method != 'POST':
        # Nie przekazano żadnych danych, należy utworzyć pusty formularz.
        form = EntryForm()
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = EntryForm(data=request.POST)
        if form.is_valid():
            new_entry = form.save(commit=False)
            new_entry.topic = topic
            new_entry.save()
            return redirect('residents_platform:topic', topic_id=topic_id)
    # Wyświetlenie pustego formularza.
    context = {'topic': topic, 'form': form}
    return render(request, 'residents_platform/new_entry.html', context)


# @login_required
# def topic_reply(request, topic_id):


@login_required
def edit_entry(request, entry_id):
    """Edycja istniejącego wpisu."""
    entry = Entry.objects.get(id=entry_id)
    topic = entry.topic

    if request.method != 'POST':
        # Żądanie początkowe, wypełnienie formularza aktualną treścią wpisu.
        form = EntryForm(instance=entry)
    else:
        # Przekazano dane za pomocą żądania POST, należy je przetworzyć.
        form = EntryForm(instance=entry, data=request.POST)
        if form.is_valid():
            form.save()
            return redirect('residents_platform:topic', topic_id=topic.id)
    context = {'entry': entry, 'topic': topic, 'form': form}
    return render(request, 'residents_platform/edit_entry.html', context)
