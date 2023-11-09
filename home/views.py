from django.shortcuts import render
from todo.models import Todo

# Create your views here.


def index_page(request):
    context = {
        'todo': Todo.objects.order_by('priority').all()
    }
    return render(request, 'home/index.html', context=context)