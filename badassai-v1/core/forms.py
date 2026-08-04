from django import forms


class HoneypotMixin(forms.Form):
    """Spam trap: a field humans never see. Any value = silently discard."""

    website = forms.CharField(required=False, widget=forms.HiddenInput)

    def is_spam(self):
        return bool(self.cleaned_data.get("website"))


class ContactForm(HoneypotMixin, forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()
    company = forms.CharField(max_length=120, required=False)
    phone = forms.CharField(max_length=40, required=False)
    message = forms.CharField(widget=forms.Textarea)


class MemberInterestForm(HoneypotMixin, forms.Form):
    name = forms.CharField(max_length=120)
    email = forms.EmailField()


class NewsletterForm(HoneypotMixin, forms.Form):
    email = forms.EmailField()
