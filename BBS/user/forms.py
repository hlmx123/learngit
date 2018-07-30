from django import forms

from user.models import User


class RegisterForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['nickname', 'password', 'icon', 'age', 'sex']

    password2 = forms.CharField(max_length=128)

    # def clean_password(self):
    #
    #     cleaned_data = super().clean()
    #     # password = cleaned_data.get('password')
    #     print(cleaned_data.get('password'))
    #     password2 = cleaned_data.get('password2')
    #     password = cleaned_data.get('password')
    #     if len(cleaned_data.get('password'))<6:
    #         raise forms.ValidationError('password too short')
    #     # else:
    #     if password != password2:
    #             raise forms.ValidationError('两次密码不一致')



    def clean_password2(self):
        '''二次密码验证'''
        cleaned_data = super().clean()
        # print(cleaned_data)
        password = cleaned_data.get('password')
        password2 = cleaned_data.get('password2')
        # print(password,password2)

        if password != password2:
                raise forms.ValidationError('两次密码不一致')
