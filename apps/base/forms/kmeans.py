from django import forms

INIT_CHOICES = (
    ('k-means++', 'k-means++'), 
    ('random', 'random')
)

class KmeansForm(forms.Form):

    query= forms.CharField(label='Query', 
        widget=forms.TextInput(attrs={
            'class': 'form-control'}))

    n_clusters= forms.IntegerField(label='Número de Clusters', 
        widget=forms.NumberInput(attrs={
            'class': 'form-control'}))

    init = forms.ChoiceField(choices=INIT_CHOICES, 
        label='Init', 
        widget=forms.Select(attrs={
        'class': 'form-control'}))

    max_iter = forms.IntegerField(label='Número de Iteraciones', initial=300,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'}))

    n_init= forms.IntegerField(label='N init', initial=10,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'}))

    random_state= forms.IntegerField(label='Semilla', initial=0,
        widget=forms.NumberInput(attrs={
            'class': 'form-control'}))