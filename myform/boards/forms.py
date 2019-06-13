from django import forms
from .models import Board


class BoardForm(forms.ModelForm):
    class Meta: # 데이터를 설명하기 위한 데이터
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
        
        # fields = '__all__'
        # exclude = ('title',)
        # widgets = {
        #     'title': forms.TextInput(
        #         attrs={
        #             'class': 'title',
        #         }
        #     )
        # }
