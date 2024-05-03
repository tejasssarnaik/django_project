
# from django import forms

# class MyForm(forms.Form):

#     select_file = forms.FilePathField(path = "E:/files/")


from django import forms

class RegistrationForm(forms.Form):
    full_name = forms.CharField(max_length=100)
    email = forms.EmailField()
    username = forms.CharField(max_length=100)
    institute_name = forms.CharField(max_length=100)
    designation = forms.CharField(max_length=100)
    password1 = forms.CharField(widget=forms.PasswordInput)
    password2 = forms.CharField(widget=forms.PasswordInput)




# Inside your app directory, create a file named forms.py
from django import forms

class FileLinkForm(forms.Form):
    file_link = forms.CharField(label='File Link',max_length=500)



## forms.py
from django import forms

class FilePathForm(forms.Form):
    file_link = forms.CharField(label='File Link', max_length=500)

