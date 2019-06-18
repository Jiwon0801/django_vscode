## Comment (Board/User)

- __boards/models.py__

```python
# Comment : User = 1:N
class Comment(models.Model):
    content = models.CharField(max_length=100)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE ) # User model 1:N
    board = models.ForeignKey(Board, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
```

```shell
python manage.py migrations
python manage.py migrate
```



- __boards/forms.py__

```python
from .models import Board, Comment

class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ('content',)
```



- __boards/admin.py__

```python
from .models import Board, Comment

class CommentAdmin(admin.ModelAdmin):
    list_display = [ 'content', 'user_id', 'board_id',]
admin.site.register(Comment, CommentAdmin)
```



- __boards/views.py__

```python
from .forms import BoardForm, CommentForm

def detail(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    comment_form = CommentForm()
    context = { 'board': board, 'comment_form':comment_form, }
    return render(request, 'boards/detail.html', context)
```



- __boards/detail.html__

```html
<h4>댓글 작성</h4>
  <form action="#" method="POST">
    {% csrf_token %}
    {{ comment_form }}
    <input type="submit" value="작성">
  </form>
```



### CREATE

- 로그인한 유저만 삭제 가능
- POST 요청에만 VIEW 함수 호출 가능
- 로그인한 유저만 댓글 작성 가능



##### views.py/comments_create

```python
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
    
```



#####  views.py/detail

```python
def detail(request, board_pk):
    # board = Board.objects.get(pk=board_pk)
    board = get_object_or_404(Board, pk=board_pk)
    
    comment_form = CommentForm()
    comments = board.comment_set.all()
    
    context = { 'board': board, 'comment_form':comment_form, 'comments': comments,}
    return render(request, 'boards/detail.html', context)
```



##### detail.html

- __dictsortreversed__ : 역순

```html
<h4>댓글</h4>
  <p>{{ comments | length }}</p>
  {% for comment in comments|dictsortreversed:"pk" %}
    <p><strong>{{ comment.user }}</strong> </p>
    <li>
      {{ comment.content}}
      <form action=""></form>
    </li>

  {% endfor %}
```





### DELETE

- 로그인한 유저만 삭제 가능
- POST 요청에만 VIEW 함수 호출 가능
- 내가 작성한 댓글만 삭제할 수 있음
- (로직) 남의 댓글은 삭제 버튼도 안보이게 해야함



##### views.py/comments_delete

```python
@login_required
@require_POST
def comments_delete(request, board_pk, comment_pk):
    # comment 받아오기
    comment = get_object_or_404(Comment, pk=comment_pk)
    if comment.user == request.user:
        comment.delete()
       
    return redirect('boards:detail', board_pk)
```



##### detail.html

```html
<h4>댓글</h4>
  {% if user.is_authenticated %}
    <p>{{ comments | length }}</p>
    {% for comment in comments|dictsortreversed:"pk" %}
      <p><strong>{{ comment.user }}</strong> </p>
      
      <li>
       {{ comment.content}}
       {% if comment.user == request.user %}
        <form action="{% url 'boards:comments_delete' board.pk comment.pk %}" method="POST" style="display:inline;">
          {% csrf_token %}
          <input type="submit" value="삭제">
        </form>
       {% endif %}   
      </li>
    {% endfor %}
  
  {% else %}
    <a href="{% url 'accounts:login'%}">댓글을 작성하려면 로그인하세요</a>

  {% endif %}
```

