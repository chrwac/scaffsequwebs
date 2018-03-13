from django import forms

class DBSequForm(forms.Form):
    order = forms.IntegerField(min_value=4,max_value=9,initial=7)
    length = forms.IntegerField(initial=7560)
    rev_comp_free = forms.BooleanField(required=False)
    init_sequ = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}))
    forbidden_sequ = forms.CharField(required=False,widget=forms.Textarea(attrs={'rows': 4, 'cols': 80}))
    email = forms.EmailField()

class RepSequForm(forms.Form):
    rep_sequ  = forms.ChoiceField(choices=[("AA","AA"),("TT","TT")])
    length_of_variable_part = forms.IntegerField(min_value=4,max_value=8,initial=5)
    email = forms.EmailField()

class MarkSequForm(forms.Form):
    mark_order = forms.IntegerField(min_value=1,max_value=4)
    sequ_length = forms.IntegerField()
    email = forms.EmailField()

class CheckSequForm(forms.Form):
    sequence = forms.CharField(widget=forms.Textarea(attrs={'rows': 8, 'cols': 80}))
    db_order = forms.IntegerField(min_value=4,max_value=9,required=False,initial=4)
    check_DB_Property = forms.BooleanField(required=False)
    check_RC_free = forms.BooleanField(required=False)

class RevCompForm(forms.Form):
    sequence = forms.CharField(widget=forms.Textarea(attrs={'rows': 8, 'cols': 80}))
    reverse = forms.BooleanField(required=False)
    complement = forms.BooleanField(required=False)
