## M:N

#### gitbash

```shell
$ python -m venv model-venv
$ source model-venv/Scripts/activate
$ django-admin startproject modelrelation .
$ python manage.py startapp manytomany
$ code .
```

#### VS Code

```shell
$ source model-venv/Scripts/activate
```

```python
# seetings.py

INSTALLED_APPS = [
    'manytomany.apps.ManytomanyConfig',
]
```

```shell
$ pip install django_extentions
```

```python
# seetings.py

INSTALLED_APPS = [
    'manytomany.apps.ManytomanyConfig',
    'django_extensions',
]
```

```shell
$ python manage.py shell_plus
```



## LIKE



## FOLLOW