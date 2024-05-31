import matplotlib.pyplot as plt
import io
import base64
from django.shortcuts import render, redirect, get_object_or_404

from .models import Question, Choice
# Create your views here.
def home(request):
    questions = Question.objects.all()
    return render(request, 'poll/home.html',
        {"questions": questions})

def vote(request, q_id):
    q = get_object_or_404(Question, pk=q_id)
    if request.method == "POST":
        try:
            choice_id = request.POST.get('choice')
            choice = Choice.objects.get(pk=choice_id)
            choice.votes += 1
            choice.save()
            return redirect('poll:result', q_id)
        except(KeyError, Choice.DoesNotExist):
            return render(request, 'poll/vote.html', {"question": q, "error_message": "Debes elegir algo"})
    return render(request, 'poll/vote.html', {"question": q})

def result(request, q_id):
    q = get_object_or_404(Question, pk=q_id)
    
    # Obtener los datos para la gráfica
    choices = q.choice_set.all()
    labels = [choice.choice_text for choice in choices]
    votes = [choice.votes for choice in choices]

    # Crear la gráfica
    fig, ax = plt.subplots()
    ax.pie(votes, labels=labels, autopct='%1.1f%%', startangle=90)
    ax.axis('equal')  # Asegura que el pastel se dibuje como un círculo.

    # Guardar la gráfica en un objeto BytesIO
    buf = io.BytesIO()
    plt.savefig(buf, format='png')
    buf.seek(0)
    graph = base64.b64encode(buf.read()).decode('utf-8')
    buf.close()

    return render(request, 'poll/result.html', {"question": q, "graph": graph})