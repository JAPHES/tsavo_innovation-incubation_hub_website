from django import forms

from .models import ContactMessage


class ContactForm(forms.ModelForm):
    website = forms.CharField(required=False, widget=forms.HiddenInput, label="Leave this field blank")
    consent = forms.BooleanField(
        required=True,
        label="I consent to TIIH storing this information to respond to my inquiry.",
    )

    class Meta:
        model = ContactMessage
        fields = ("full_name", "email", "phone", "subject", "message", "consent")
        widgets = {
            "full_name": forms.TextInput(attrs={"autocomplete": "name"}),
            "email": forms.EmailInput(attrs={"autocomplete": "email"}),
            "phone": forms.TextInput(attrs={"autocomplete": "tel"}),
            "message": forms.Textarea(attrs={"rows": 6}),
        }

    def clean_website(self):
        value = self.cleaned_data.get("website", "")
        if value:
            raise forms.ValidationError("Unable to submit this form.")
        return value
