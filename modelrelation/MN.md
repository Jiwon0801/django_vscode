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



- __models.py__

```python
from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.TextField()

    def __str__(self):
        return f'{self.pk}번 의사 {self.name}'


class Patient(models.Model):
    name = models.TextField()

    def __str__(self):
        return f'{self.pk}번 환자 {self.name}'

# 중개모델
class Reservation(models.Model):
    doctor = models.ForeignKey(Doctor, on_delete=models.CASCADE)
    patient = models.ForeignKey(Patient, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.doctor_id}번 의사의 {self.patient_id}번 환자'
```



- shell_plus

```sqlite
doctor = Doctor.objects.create(name="Kim")
patient = Patient.objects.create(name="John")
Reservation.objects.create(doctor=doctor, patient=patient)

patient.reservation_set.all()
```



-  __중개모델 연결__

```python
from django.db import models

# Create your models here.
class Doctor(models.Model):
    name = models.TextField()

    def __str__(self):
        return f'{self.pk}번 의사 {self.name}'


class Patient(models.Model):
    name = models.TextField()
    # 중개 모델인 Reservation을 연결
    doctors = models.ManyToManyField(Doctor, related_name='patients')

    def __str__(self):
        return f'{self.pk}번 환자 {self.name}'

# 중개 모델 클래스 없어도 테이블 생성됨


```

```python
pip install ipyhon

In [1]: doctor = Doctor.objects.create(name='Kim')

In [2]: patient = Patient.objects.create(name='John')

In [3]: doctor.patients.add(patient)

In [4]: patient.doctors.add(doctor)

In [5]: doctor.patients.remove(patient)
```

