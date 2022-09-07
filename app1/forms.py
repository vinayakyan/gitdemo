from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.contrib.auth import password_validation, authenticate
from .models import Post


class MyUserCreationForm(UserCreationForm):
    first_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'e.g John'
    }))
    last_name = forms.CharField(max_length=20, widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'e.g Elder'
    }))
    username = forms.CharField(label='Username', widget=forms.TextInput(attrs={
        'class': 'form-control', 'placeholder': 'e.g John'
    }), help_text='Required. 150 characters or fewer. Letters, digits and @/./+/-/_ only.', max_length=150)

    password1 = forms.CharField(
        label="Password",
        strip=False,
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        help_text=password_validation.password_validators_help_text_html(),
    )
    password2 = forms.CharField(
        label="Password confirmation",
        widget=forms.PasswordInput(attrs={"autocomplete": "new-password", 'class': 'form-control'}),
        strip=False,
        help_text="Enter the same password as before, for verification.",
    )
    email = forms.EmailField(label='Email Address', widget=forms.EmailInput(attrs={
        'class': 'form-control'
    }), help_text='We will never share your email with anyone')

    class Meta:
        fields = ('username', 'first_name', 'last_name', 'password1', 'password2', 'email')
        model = User


class LoginForm(forms.Form):
    username = forms.CharField(max_length=150, label='Username', widget=forms.TextInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'enter the username'
        }
    ))
    password = forms.CharField(label='Password', widget=forms.PasswordInput(
        attrs={
            'class': 'form-control',
            'placeholder': 'enter the password'
        }
    ), help_text='Password is Case Sensitive')

    error_messages = {
        "invalid_login": (
            "Please enter a correct %(username)s and password. Note that both "
            "fields may be case-sensitive."
        ),
        "inactive": "This account is inactive.",
    }

    def clean(self):
        username = self.cleaned_data['username']
        password = self.cleaned_data['password']

        if username is not None and password:
            self.user_cache = authenticate(username=username, password=password)
            if self.user_cache is None:
                raise forms.ValidationError(self.error_messages['invalid_login'],
                                            code='invalid login',
                                            params={'username': 'username'})
            else:
                if not self.user_cache.is_active:
                    raise forms.ValidationError(
                        self.error_messages["inactive"],
                        code="inactive",
                    )
            return self.cleaned_data


class PostForm(forms.ModelForm):

    class Meta:
        model = Post
        fields = '__all__'
        exclude = ('created_by',)
        widgets = {
            'title': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter Title Here'
            }),
            'content': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Enter The Content Here'
            })
        }
