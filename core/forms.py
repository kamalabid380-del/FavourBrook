from django import forms

from .models import ContactMessage, Order


class CheckoutForm(forms.ModelForm):
    class Meta:
        model = Order
        fields = ["name", "email", "phone", "address", "city", "notes"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Full name", "autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com", "autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"placeholder": "+44 …", "autocomplete": "tel"}),
            "address": forms.Textarea(attrs={"rows": 3, "placeholder": "Street address", "autocomplete": "street-address"}),
            "city": forms.TextInput(attrs={"placeholder": "Town / City", "autocomplete": "address-level2"}),
            "notes": forms.Textarea(attrs={"rows": 2, "placeholder": "Delivery notes (optional)"}),
        }


class ContactForm(forms.ModelForm):
    class Meta:
        model = ContactMessage
        fields = ["name", "email", "phone", "message"]
        widgets = {
            "name": forms.TextInput(attrs={"placeholder": "Full name"}),
            "email": forms.EmailInput(attrs={"placeholder": "you@example.com"}),
            "phone": forms.TextInput(attrs={"placeholder": "Phone (optional)"}),
            "message": forms.Textarea(attrs={"rows": 5, "placeholder": "How can we help?"}),
        }