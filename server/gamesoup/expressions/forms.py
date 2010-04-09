from django import forms


class ExpressionForm(forms.Form):    
    expr = forms.CharField(label='Expression', required=True)
