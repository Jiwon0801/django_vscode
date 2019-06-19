## FOLLOW

- User : User = M:N


- User django를 기본적으로 제공해준  user
- 새로운 user 모델을 만들어 쓸 때 django가 따로 쓰는 user 모델 제공





### AbstractUser

`models.Model -> AbstractBaseUser -> AbstractUser->User`





###  Custom User  모델 대체하기

__syntax: [Djang-Tutorial_맞춤 User](<https://docs.djangoproject.com/ko/2.2/topics/auth/customizing/#substituting-a-custom-user-model>)__



- accounts/models.py

```python
from django.db import models
from django.conf import settings
from django.contrib.auth.models import AbstractUser

class User(AbstractUser):
    followers = models.ManyToManyField(settings.AUTH_USER_MODEL, related_name='followings')
```



- accounts/admin.py

```python
from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

admin.site.register(User, UserAdmin)
```



- settings.py

```python
# 맨 마지막 코드 바로 위
AUTH_USER_MODEL = 'accounts.User' #default
```



###  Custom User  auth forms

__syntax: [Djang-Tutorial_auth forms](<https://docs.djangoproject.com/ko/2.2/topics/auth/customizing/#custom-users-and-the-built-in-auth-forms>)__



- accounts/forms.py

```python
from django.contrib.auth.forms import UserChangeForm, UserCreationForm
from django.contrib.auth import get_user_model

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = get_user_model()
        fields = UserCreationForm.Meta.fields
```





- profile.html

```html
<!-- board: comment = 1: N -->
<p class="card-text">{{ board.like_users.all | length }} 명이 좋아합니다.</p>
<p class="card-text">{{ board.comment_set.all | length }} 개의 댓글.</p>
```



```html
<!-- board: comment = M: N -->
<p class="mb-0">{{ comment.board }}</p>
<footer class="blockquote-footer">{{ comment }}</footer>
```





#### 의존성파일

#####  의존성 파일 만들기

```shell
$ pip freeze > requirements.tx
```


##### 파일 받기
```
source ----
pip install -r requirements.txt
migrate
```



