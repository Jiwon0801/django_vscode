from django.shortcuts import render, redirect
from .models import Board

# Create your views here.
def index(request):
    boards = Board.objects.order_by('-pk')
    context = {'boards': boards}
    return render(request, 'boards/index.html', context)

def create(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        board = Board(title=title, content=content)
        board.save()
        return redirect('boards:index')
    else:
        return render(request, 'boards/create.html')

def detail(request, board_pk):
    board = Board.objects.get(pk=board_pk)
    context = { 'board': board}
    return render(request, 'boards/detail.html', context)
