## ORM 목록

1. __board.user:  게시글을 작성한 유저 (1:n)__
2. __board.like_users: 게시글을 좋아요한 유저들(m:n)__
3. __user.board_set: 유저가 작성한 게시글들(1:n)__
4. __user.like_boards: 유저가 좋아요한 게시글들(m:n) - related_name__





## LIKE

- user 는 여러 board에 like 할 수 있음
- board는 여러 user로부터 like 받을 수 있음
- User : Board = M:N



- 나(board)를 좋아요 한 모든 유저

  - __board.like_users.all()__

  - 내가 쓴 모든 글 가져오기

    ```python
    user.board_set.all() # 1:1관계 user에서 사용 중
    ```

  - 내가 좋아요한 모든 글들 

    ```python
    user.like_boards.all() # 역참조의 오류로 인해 무조건 related_name 사용
    ```



#### MYFORM

##### models.py

```python
class Board(models.Model):
   models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='like_boards', blank=True)
   # 글이 작성 될 때 좋아요는 빈값이므로 Null 값을 추가하기 위해 blank=True

    def __str__(self):
        return self.title
```



##### views.py

~~~python
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

~~~

##### index.html

```html
<a href="{% url 'boards:like' board.pk %}">
      {% if user in board.like_users.all %}
        <i class="fas fa-heart" style = "color: crimson"></i>
      {% else %}
        <i class="fas fa-heart" style = "color: black"></i>
      {% endif %}     
</a>
{{ board.like_users.all | length }} 명이 좋아합니다.
    
```



#### SQLite

```shell
Ctril+Shift+P

SQLite OpenDatabase
```



#### html Modulation

##### index.html

```html
{% for board in boards %}
     <!-- _board.html -->
     {% include "boards/_board.html" %}
{% endfor %}
```



##### _board.html

```html
<div class="card">
  <div class="card-header">
    작성자:{{ board.user }}
  </div>
  <div class="card-body">
    <h5 class="card-title">{{ board.title }}</h5>
    <p class="card-text">
      <a href="{% url 'boards:like' board.pk %}">
        {% if user in board.like_users.all %}
          <i class="fas fa-heart" style = "color: crimson"></i>
        {% else %}
          <i class="fas fa-heart" style = "color: black"></i>
        {% endif %}     
    </a>
    {{ board.like_users.all | length }} 명이 좋아합니다.  
    </p>
    <a href="{% url 'boards:detail' board.pk %}" class="btn btn-primary">글 상세보기</a>
  </div>
</div>

<hr>

```




## FOLLOW

- User : User = M:N



## Profile