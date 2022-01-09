from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import User, ShippingAddress, PaymentInfo


class SignUpForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super(SignUpForm, self).__init__(*args, **kwargs)

        self.fields['password1'].widget.attrs['class'] = 'form-input'
        self.fields['password2'].widget.attrs['class'] = 'form-input'

    class Meta:
        model = User
        fields = ['name', 'email', 'cell_number', 'password1', 'password2']
        widgets = {
            'name': forms.TextInput(),
            'email': forms.EmailInput(),
            'cell_number': forms.NumberInput(),
            # 'profile_picture': forms.FileInput(),
            'password1': forms.PasswordInput(),
            'password2': forms.PasswordInput()
        }


class ShippingAddressForm(forms.ModelForm):
    class Meta:
        model = ShippingAddress
        fields = ['first_name', 'last_name', 'company_name', 'area_code', 'primary_phone', 'street_address', 'zip_code']

    def clean(self):
        return self.cleaned_data


# class PaymentInfoForm(forms.ModelForm):
#     class Meta:
#         model = PaymentInfo
#         fields = ['carholder_name', 'card_number', 'expiration_date', 'csc_number']


class UserAccountUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['email', 'cell_number']
        widgets = {
            'email': forms.EmailInput(),
            'password': forms.PasswordInput()
        }
