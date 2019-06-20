# VScode_Django



### Gitbash 폴더 만들기



### 가상환경 설정

```shell
student@M9037 MINGW64 ~/Desktop/jiwon/Django_VS/myform
$ python -m venv form-venv #가상환경설정

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
'bootstrap4',
```



```html
{% load bootstrap4 %}

{# Display a form #}

<!doctype html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport"
          content="width=device-width, user-scalable=no, initial-scale=1.0, maximum-scale=1.0, minimum-scale=1.0">
    <meta http-equiv="X-UA-Compatible" content="ie=edge">
    {% bootstrap_css %}
    <link rel="stylesheet" href="https://stackpath.bootstrapcdn.com/bootstrap/4.3.1/css/bootstrap.min.css" integrity="sha384-ggOyR0iXCbMQv3Xipma34MD+dH/1fQ784/j6cY/iJTQUOhcWr7x9JvoRxT2MZw1T" crossorigin="anonymous">
    {% block css %}{% endblock %}
    <title>Document</title>
</head>
<body>
    <h1></h1>
    <hr>
    <div class = "container">
        {% block content %}
        {% endblock %}
    </div>
   
{% bootstrap_javascript jquery='full' %}
</body>
 
</html>
```

