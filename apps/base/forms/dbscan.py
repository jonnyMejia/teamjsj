from django import forms

class DBScanForm(forms.Form):
    eps= forms.DecimalField(label='EPS', 
        widget=forms.NumberInput(attrs={
            'class': 'form-control'}))

    min_samples = forms.IntegerField(label='Minimo de ejemplos', 
        widget=forms.NumberInput(attrs={
            'class': 'form-control'}))