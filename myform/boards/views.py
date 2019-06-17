from django.shortcuts import render, redirect, get_object_or_404
from IPython import embed
from django.contrib.auth.decorators import login_required
from .models import Board
from .forms import BoardForm

# Create your views here.
def index(request):
    boards = Board.objects.order_by('-pk')
    context = {'boards': boards}
    return render(request, 'boards/index.html', context)

@login_required
def create(request):
    if request.method == 'POST':
        # DATA Binding: form 인스턴스 생성하고 요청 (request.POST)로 데이터를 채운다.
        form = BoardForm(request.POST)
        # form  유효성 체크
        if form.is_valid():
            # # cleaned_data는 queryDict를  return 하기 때문에 .get으로 접근 가능
            # title = form.cleaned_data.get('title')
            # content = form.cleaned_data.get('content')
            # # 검증을 통과한 꺠끗한 데이터를 form에서 가져와 board 인스턴스를 만든다.
            # board = Board.objects.create(title=title, content=content)
            board = form.save()
            return redirect('boards:detail', board.pk)
    # GET : 기본 form 인스턴스를 생성
    else:
        form = BoardForm()
    # GET : 기본 form 모습으로 넘겨짐
    # POST : 요청에서 검증이 실패한 form은 오류메세지를 포함된 상태로 넘겨짐
    context = {'form':form}
    return render(request, 'boards/form.html', context)

def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    context = { 'board': board}
    return render(request, 'boards/detail.html', context)


def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method=='POST':
        board.delete()
        return redirect('boards:index')
    else:
        return redirect('boards:detail', board.pk)

@login_required
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method=='POST':
        # form에서 이미 존재하는 경우에는 instance  사용
        form = BoardForm(request.POST, instance = board)
        if form.is_valid():
            # board.title = form.cleaned_data.get('title')
            # board.content = form.cleaned_data.get('content')
            # board.save()
            board = form.save()
            return redirect('boards:detail', board.pk)
    else:
        #form = BoardForm(initial=board.__dict__)
        form = BoardForm(instance=board)

    
    context = {'form':form, 'board' : board,}
    return render(request, 'boards/form.html', context)
