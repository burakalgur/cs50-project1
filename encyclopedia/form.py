from django import forms

class CreateForm(forms.Form):
    title = forms.CharField(label="Title")
    content = forms.CharField(widget=forms.Textarea(attrs={ 'style': 'height: 500px;'}))

class EditForm(forms.Form):
    content = forms.CharField(widget=forms.Textarea(attrs={ 'style': 'height: 500px;'}))
    
    def __init__(self, *args, **kwargs):
        initial_content = kwargs.pop('initial_content')
        super(EditForm, self).__init__(*args, **kwargs)
        self.fields['content'].initial = initial_content