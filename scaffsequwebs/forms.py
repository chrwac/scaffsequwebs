from django import forms

class DBSequForm(forms.Form):
    order = forms.IntegerField(min_value=4,max_value=9)
    circular = forms.BooleanField(required=False)
    init_sequ = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}))
    forbidden_sequ = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}))
    email = forms.EmailField()

class RepSequForm(forms.Form):
    mark_order = forms.IntegerField(min_value=1,max_value=4)
    email = forms.EmailField()

class MarkSequForm(forms.Form):
    mark_order = forms.IntegerField(min_value=1,max_value=4)
    sequ_length = forms.IntegerField()
    email = forms.EmailField()

class CheckSequForm(forms.Form):
    sequence = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows': 8, 'cols': 80}))
