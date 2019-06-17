# Authentication



### 새로운 app  생성



### sign up (UserCreationForm)

- __CRUD Create에 해당__
- __User  모델을 만들 필요가 없다.__

```python
from django.contrib.auth.forms import UserCreationForm


 def signup(request):
    if request.method == 'POST' :
        pass
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'accounts/signup.html', context)
```

​	

### Login (AuthenticationForm)

- __Session Create__
- __쿠키__
  - 클라이언트에 저장되는 키-값 데이터 파일. 일정시간 동안 데이터 저장 가능
  - 웹페이지에 접속하면 쿠키를 로컬에 저장하고 클라이언트가 재요청시에 웹페이지 요청과 함께 쿠키 값도 같이 전송
  - 자동 로그인, 팝업 체크 정보, 장바구니
  - 개인정보는 쿠키에 저장할 수 없다. -> Session으로 해결
- __세션(서버)__
  - 일정 시간동안 같은 클라이언트로부터 들어오는 요청을 하나의 상태로 보고 유지하는 기술
  - __클라이언트 ID 는 쿠키에도 저장되고 세션에도 저장된다.__
  - 클라이언트(세션쿠키) -> 세션 전달

```python
from django.contrib.auth import login as auth_login  #session create

def login(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, request.POST)
        if form.is_valid():
            auth_login(request, form.get_user()) # user session create
            return redirect('boards:index')
    else:
        form = AuthenticationForm
    context = {'form': form}
    return render(request, 'accounts/login.html', context)

```

### Logout

- __Session delete__

```python
from django.contrib.auth import logout as auth_logout

def logout(request):
    auth_logout(request)
    return redirect('boards:index')      


```

### 회원 탈퇴

- __User delete__

```python
def delete(request):
    if request.method == 'POST':
        request.user.delete()
    return redirect('boards:index')
```



### 회원 수정 (UserChangeForm)

```python
from django.contrib.auth.forms import UserChangeForm

def update(request):
    if request.method == 'POST':
        form = UserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('boards:index')
    else:
        form = UserChangeForm(instance=request.user) # 기존 정보 필요 하므로 instance
    context = {'form': form,}
    return render(request, 'accounts/update.html', context)
```

- 너무 많은 내용이 ChangeForm에 나와있기 때문에 Custom 만들기

```python
#accounts/forms.py

from django.contrib.auth.forms import UserChangeForm
from django.contrib.auth import get_user_model

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = get_user_model()
        fields = ('email', 'first_name', 'last_name',)
```

```python
#accounts/views.py
from .forms import CustomUserChangeForm

def update(request):
    if request.method == 'POST':
        form = CustomUserChangeForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('boards:index')
    else:
        form = CustomUserChangeForm(instance=request.user) # 기존 정보 필요 하므로 instance
    context = {'form': form,}
    return render(request, 'accounts/auth_form.html', context)
```





### 비밀번호 변경(PasswordChangeForm)

```python
def change_password(request):
    if request.method=='POST':
        form = PasswordChangeForm(request.user, request.POST)
        if form.is_valid():
            user = form.save()
            # 현재 사용자의 인증 세션이 무효화 되는 것을 막고 세션을 유지하게 만들어준다.
            update_session_auth_hash(request, user)
            return redirect('boards:index')
    else:
        form = PasswordChangeForm(request.user)
    context = {'form': form,}
    return render(request, 'accounts/change_password.html', context)
```





### Authorization

- __위임, 권한부여__

- 비로그인 상태로  create와 update로 넘어갈 수 있음
- 처리되면 login 페이지로 넘어감

```python
# base/views.py
from django.contrib.auth.decorators import login_required

@login_required
def create(request):
    
@login_required
def update(request, board_pk):

```



### html 중복 제거

```html
#accounts/auth_form.html

{% if request.resolver_match.url_name == 'signup' %}
  <h1>회원가입</h1>
{% elif request.resolver_match.url_name == 'login' %}
  <h1>로그인</h1>
{% elif request.resolver_match.url_name == 'update' %}
  <h1>회원수정</h1>
{% else %}
  <h1>비번변경</h1>
{% endif %}
```



```python
# accounts/views.py

return render(request, 'accounts/auth_form.html', context)
```



###  User model

```python
# boards/models.py
from django.conf import settings

class Board(models.Model):
      user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
```



### 로직 수정

- 남의 글 수정, 삭제 못하게 막기

```python
def delete(request, board_pk):
    board = get_object_or_404(Board, pk=board_pk)
    # if-else 감싸기
    if board.user == request.user: 
        if request.method=='POST':
            board.delete()
            return redirect('boards:index')
        else:
            return redirect('boards:detail', board.pk)
    else:
        return redirect('boards:index')
```





#### VS CODE sqlite extension download

