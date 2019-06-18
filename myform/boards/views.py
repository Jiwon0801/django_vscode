from django.shortcuts import render, redirect, get_object_or_404
from IPython import embed
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from .models import Board, Comment
from .forms import BoardForm, CommentForm

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
            

            board = form.save(commit=False)
            board.user = request.user
            
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
    
    comment_form = CommentForm()
    comments = board.comment_set.all()
    
    context = { 'board': board, 'comment_form':comment_form, 'comments': comments,}
    return render(request, 'boards/detail.html', context)


def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user: 
        if request.method=='POST':
            board.delete()
            return redirect('boards:index')
        else:
            return redirect('boards:detail', board.pk)
    else:
        return redirect('boards:index')

@login_required
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if board.user == request.user : 
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

    else:
        return redirect('boards:index')

    context = {'form':form, 'board' : board,}
    return render(request, 'boards/form.html', context)


# 로그인 된 유저만 작성 가능
@login_required
# POST 요청으로만 작성 가능
@require_POST
def comments_create(request, board_pk):
    comment_form = CommentForm(request.POST)
    if comment_form.is_valid():      
        # 바로 DB에 바로 저장하지 않고 외래키 값을 갖고 오기 위해 commit=False
        comment = comment_form.save(commit=False)
        comment.user = request.user
        comment.board_id = board_pk
         # DB 저장
        comment.save()
    return redirect('boards:detail', board_pk) 
    

@login_required
@require_POST
def comments_delete(request, board_pk, comment_pk):
    # comment 받아오기
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
       
    return redirect('boards:detail', board_pk)


@login_required
def like(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    user = request.user
    # 해당 게시글에 좋아요를 누른 사용자 중에 현재 요청을 한 사용자가 존재한다면 (이미 좋아요 누른 상태)
    if board.like_users.filter(pk=request.user.pk).exists():
    # if user in board.like_users.all():
       # 좋아요를 취소하고
       board.like_users.remove(user)
    # 좋아요를 누르지 않은 상태라면
    else:
        # 좋아요를 누름
        board.like_users.add(user)
    return redirect('boards:index')

   