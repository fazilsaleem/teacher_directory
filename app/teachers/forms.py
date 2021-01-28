
from django import forms
from teachers.models import Teachers, Subjects

class TeacherProfileForm(forms.ModelForm):
    subjects_taught = forms.ModelMultipleChoiceField(
            queryset=Subjects.objects.all(),
            widget=forms.CheckboxSelectMultiple
        )
    email = forms.EmailField(max_length = 200) 

    class Meta:
        model = Teachers
        fields = ('first_name', 'last_name','email','phone_number','room_number','subjects_taught','profile_picture')        
        
    def __init__(self, *args, **kwargs):
        super(TeacherProfileForm, self).__init__(*args, **kwargs)
        for key in self.fields:
            if not  key=="subjects_taught":
                self.fields[key].widget.attrs['class'] = "form-control"
        self.fields['first_name'].widget.attrs['required'] = True
        self.fields['last_name'].widget.attrs['required'] = True
        self.fields['email'].widget.attrs['required'] = True
        self.fields['room_number'].widget.attrs['required'] = True
        self.fields['subjects_taught'].widget.attrs['class'] = "subject-check"
        