## Social Login



### 설정

__syntax: [django-allauth](<https://django-allauth.readthedocs.io/en/latest/installation.html>)__

```shell
pip install django-allauth
```

- __settings.py__

```python
INSTALLED_APPS = [    
    'django.contrib.sites',
    'allauth',
    'allauth.account',
    'allauth.socialaccount',
    'allauth.socialaccount.providers.kakao',    
]

SITE_ID = 1
```

- __urls.py__

```python
urlpatterns = [
    path('accounts/', include('accounts.urls')),
    # allauth는 기존 accounts 보다 밑에 있어야 함
    path('accounts/', include('allauth.urls')),
]
```




- __kakao Redirect Path __

  __syntax:[kakao](<https://django-allauth.readthedocs.io/en/latest/providers.html?highlight=kakao#kakao>)__

```html
/accounts/kakao/login/callback/
```



- __accounts/login.html__

  __syntax: [Provider-Facebook](<https://django-allauth.readthedocs.io/en/latest/providers.html?highlight=login_url>)__

```html
{% load socialaccount %}

<a href="{% provider_login_url "kakao" method="oauth2" %}">KAKAO LOGIN</a>

```

- __settings.py__

```python
# 기존
STATIC_URL = '/static/'

LOGIN_REDIRECT_URL = 'board:index'
```

