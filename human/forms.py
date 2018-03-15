from django import forms

class QuickSearchForm(forms.Form):
    quick_search = forms.CharField(label="quick search", max_length=100)