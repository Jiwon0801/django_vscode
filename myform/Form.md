# Form



### forms.py

```python
from django import forms

#form 이용
class BoardForm(forms.Form):
    title = forms.CharField(
        max_length=10,
        label='제목',
        widget = forms.TextInput(
            attrs={
                'class':'title',
                'placeholder': 'Enter the title',
            }))
    content = forms.CharField(
        label='내용',
        widget = forms.Textarea(
            attrs={
                'class': 'content-type',
                'rows' : 5,
                'cols' : 50,
                'placeholder' : 'Enger the content',
            }
        )
    )
```



### CREATE

- __create.html__

  ```python
  {% extends 'boards/base.html' %}
  {% block content %}
    <h1>CREATE</h1>
    <form action="{% url 'boards:create' %}" method = "POST">
      {% csrf_token %}
      <label for="title">TITLE</label>
      <input type="text" name="title" id="ttitle">
      <label for="content">CONTENT</label>
      <input type="text" name="content" id="content"> 
      <input type="submit" value="Submit">
    </form>
  {% endblock  %}
  ```

  

  - __form 적용__

    ```python
    {% extends 'boards/base.html' %}
    {% block content %}
    <h1>CREATE</h1>
    <form action="" method = "POST">
      {% csrf_token %}
      {{ form.as_p }}
      <input type="submit" value="Submit">
    </form>
    {% endblock  %}
    ```




- __views.py__
  
  ```python
  def create(request):
      if request.method == 'POST':
          # DATA Binding: form 인스턴스 생성하고 요청 (request.POST)로 데이터를 채운다.
          form = BoardForm(request.POST)
          # form  유효성 체크
          if form.is_valid():
              # cleaned_data는 queryDict를  return 하기 때문에 .get으로 접근 가능
              title = form.cleaned_data.get('title')
              content = form.cleaned_data.get('content')
              # 검증을 통과한 꺠끗한 데이터를 form에서 가져와 board 인스턴스를 만든다.
              board = Board.objects.create(title=title, content=content)
              board = form.save()
              return redirect('boards:detail', board.pk)
      # GET : 기본 form 인스턴스를 생성
      else:
          form = BoardForm()
      # GET : 기본 form 모습으로 넘겨짐
      # POST : 요청에서 검증이 실패한 form은 오류메세지를 포함된 상태로 넘겨짐
      context = {'form':form}
      return render(request, 'boards/create.html', context)
  ```
  
  
  
  - __form 적용__
  
    ```python
    def create(request):
        if request.method == 'POST':
            # DATA Binding: form 인스턴스 생성하고 요청 (request.POST)로 데이터를 채운다.
            form = BoardForm(request.POST)
            # form  유효성 체크
            if form.is_valid():
                board = form.save()
                return redirect('boards:detail', board.pk)
        # GET : 기본 form 인스턴스를 생성
        else:
            form = BoardForm()
        # GET : 기본 form 모습으로 넘겨짐
        # POST : 요청에서 검증이 실패한 form은 오류메세지를 포함된 상태로 넘겨짐
        context = {'form':form}
        return render(request, 'boards/create.html', context)
    ```
  
    
### UPDATE

- __views.py  form 적용__  

```python
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method=='POST':
        form = BoardForm(request.POST)
        if form.is_valid():
            board.title = form.cleaned_data.get('title')
            board.content = form.cleaned_data.get('content')
            board.save()
            
            return redirect('boards:detail', board.pk)
    else:
        form = BoardForm(initial=board.__dict__)

    
    context = {'form':form, 'board' : board,}
    return render(request, 'boards/form.html', context)
```






#  ModelForm



### forms.py

```python
class BoardForm(forms.ModelForm):
    class Meta: # 데이터를 설명하기 위한 데이터
        model = Board
        fields = ('title', 'content')      
        # fields = '__all__'  # 필드에 있는 모든 값 
        # exclude = ('title',) # 제외 시키기
```



```python
from django import forms
from .models import Board


class BoardForm(forms.ModelForm):
    class Meta: # 데이터를 설명하기 위한 데이터
        #widget은 보통 위에서 지정
        title = forms.CharField(
            label = '제목',
            widget = forms.TextInput(
                attrs = {
                    'placeholder': 'Enter the title',
                }
            )
        )
        content = forms.CharField(
            label = '내용',
            widget = forms.TextInput(
                attrs = {
                    'placeholder' : 'Enter the content',
                    'rows':5,
                    'cols': 50,
                }
            )
        )
        model = Board
        fields = ('title', 'content')
```



### UPDATE

- __views.py  model form__

```python
def update(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    if request.method=='POST':
        # form에서 이미 존재하는 경우에는 instance  사용
        form = BoardForm(request.POST, instance = board)
        if form.is_valid():
            board = form.save()
            return redirect('boards:detail', board.pk)
    else:
       form = BoardForm(instance=board)

    
    context = {'form':form, 'board' : board,}
    return render(request, 'boards/form.html', context)

```



- __create.html -> form.html__

  ```html
  {% extends 'boards/base.html' %}
  {% load bootstrap4 %}
  {% block content %}
  {% comment %}
  url 정보가 creat 면 creat 출력
  update 면 update 출력
  {% endcomment %}
  
  {% if request.resolver_match.url_name == 'create' %}
    <h1>CREATE</h1>
  {% else %}
    <h1>UPDATE</h1>
  {% endif %}
    
    <form action="" method = "POST">
      {% csrf_token %}
      {% bootstrap_form form layout='horizontal'%}
      {% buttons %}
    {% buttons submit='OK' reset="Cancel"  button_class="btn-primary" %}{% endbuttons %}
    {% endbuttons %}
    
    </form>
  
    
  {% if request.resolver_match.url_name == 'create' %}
    <a href="{% url 'boards:index' %}"> back </a>
  {% else %}
    <a href="{% url 'boards:detail' board.pk %}"> back </a>
  {% endif %}
  
  {% endblock  %}
  ```

  



## FBV -  Function Based View

- CBV 보다는 코드작성이 더 있지만 개발자 스타일 대로 수정하기 용이

## CBV - Class Based View

- 코드가 매우 짧고 장고가 해주는게 굉장히 만지만 자유도가 떨어짐



