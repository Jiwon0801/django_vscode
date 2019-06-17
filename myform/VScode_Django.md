# VScode_Django



### Gitbash 폴더 만들기



### 가상환경 설정

```shell
student@M9037 MINGW64 ~/Desktop/jiwon/Django_VS/myform
$ python -m venv form-vent #가상환경설정

$ source form-venv/Scripts/activate # 가상환경동작
(form-venv)

$ python manage.py migrate

$ deactivate
```



# Bootstrap4



#### Installation

- install using pip

```shell
pip install django-bootstrap4
```

- Add to 'INSTALLED_APPS' in your 'settings.py'

```
'bootstrap4'
```



```html
{% load bootstrap4 %}

{# Display a form #}

<form action="/url/to/submit/" method="post" class="form">
    {% csrf_token %}
    {% bootstrap_form form %}
    {% buttons %}
        <button type="submit" class="btn btn-primary">Submit</button>
    {% endbuttons %}
</form>
```

