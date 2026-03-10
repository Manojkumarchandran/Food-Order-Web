from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import UserProfile, Review


class RegisterForm(UserCreationForm):
    email = forms.EmailField(required=True)
    first_name = forms.CharField(max_length=50)
    last_name = forms.CharField(max_length=50)

    class Meta:
        model = User
        fields = ('username', 'first_name', 'last_name', 'email', 'password1', 'password2')

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        if commit:
            user.save()
        return user


class UserProfileForm(forms.ModelForm):
    class Meta:
        model = UserProfile
        fields = ('phone', 'address', 'city', 'zip_code', 'avatar')
        widgets = {
            'address': forms.Textarea(attrs={'rows': 3}),
        }


class CheckoutForm(forms.Form):
    PAYMENT_METHOD_CHOICES = [
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash on Delivery'),
        ('wallet', 'Digital Wallet'),
    ]

    delivery_address = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Enter your full delivery address'})
    )
    delivery_city = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={'placeholder': 'City'})
    )
    delivery_zip = forms.CharField(
        max_length=10,
        widget=forms.TextInput(attrs={'placeholder': 'ZIP Code'})
    )
    phone = forms.CharField(
        max_length=15,
        widget=forms.TextInput(attrs={'placeholder': '+1 234 567 8900'})
    )
    payment_method = forms.ChoiceField(
        choices=PAYMENT_METHOD_CHOICES,
        widget=forms.RadioSelect
    )
    special_instructions = forms.CharField(
        required=False,
        widget=forms.Textarea(attrs={'rows': 2, 'placeholder': 'Any special requests or instructions?'})
    )


class ReviewForm(forms.ModelForm):
    rating = forms.ChoiceField(
        choices=[(i, f'{i} Star{"s" if i > 1 else ""}') for i in range(1, 6)],
        widget=forms.RadioSelect
    )

    class Meta:
        model = Review
        fields = ('rating', 'comment')
        widgets = {
            'comment': forms.Textarea(attrs={'rows': 3, 'placeholder': 'Share your experience...'}),
        }
