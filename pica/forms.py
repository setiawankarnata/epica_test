from django import forms
from .models import Company, Peserta, Topik, DivDept, Meeting, Forum, Activity

KATEGORI = [
    (None, ''),
    ('1', 'Nama Topik'),
    ('2', 'Problem'),
    ('3', 'Action'),
    ('4', 'Meeting Forum'),
    ('5', 'Status'),
    ('6', 'Function'),
    ('7', 'Company'),
    ('8', 'PIC'),
]

forums = Forum.objects.all().values_list('nama_forum', 'nama_forum')
pil = []
for forum in forums:
    pil.append(forum)


class SearchTopikForm(forms.Form):
    kategory = forms.ChoiceField(choices=KATEGORI, initial='')
    nama_query = forms.CharField(label='Query', widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50)
    period1 = forms.DateField(label='Start periode :',
                              widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},
                                                     format='%Y-%m-%d'))
    period2 = forms.DateField(label='End periode :',
                              widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},
                                                     format='%Y-%m-%d'))


class SearchAllForm(forms.Form):
    cari = forms.CharField(label='Search berdasarkan topik, problem dan action',
                           widget=forms.TextInput(attrs={'class': 'form-control'}), max_length=50)


class HistoryMeetingForm(forms.Form):
    forum = forms.ChoiceField(choices=pil, initial='')
    period1 = forms.DateField(label='Start periode :',
                              widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},
                                                     format='%Y-%m-%d'))
    period2 = forms.DateField(label='End periode :',
                              widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},
                                                     format='%Y-%m-%d'))


class ListOpenPicaForm(forms.Form):
    forum = forms.ChoiceField(choices=pil, initial='')
    period1 = forms.DateField(label='Start periode :',
                              widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},
                                                     format='%Y-%m-%d'))
    period2 = forms.DateField(label='End periode :',
                              widget=forms.DateInput(attrs={'class': 'form-control', 'type': 'date'},
                                                     format='%Y-%m-%d'))


class CreateForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = "__all__"
        widgets = {
            'nama_forum': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Forum'}),
            'keterangan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Keterangan'}),
        }


class UpdateForumForm(forms.ModelForm):
    class Meta:
        model = Forum
        fields = '__all__'
        widgets = {
            'nama_forum': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama Forum'}),
            'keterangan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Keterangan'}),
        }


class CreateMeetingForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = "__all__"
        exclude = ["meeting2peserta"]
        widgets = {
            'meeting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'),
            'notulen': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama'}),
            'location': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Location'}),
            'meeting2forum': forms.Select(attrs={'class': 'form-control', 'placeholder': 'Forum'}),
        }


class UpdateDepartemenForm(forms.ModelForm):
    class Meta:
        model = DivDept
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama divisi/departemen'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


class CreateDepartemenForm(forms.ModelForm):
    class Meta:
        model = DivDept
        fields = '__all__'
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama divisi/departemen'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'}),
        }


class CreateActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ('activity2topik', 'activity2user', 'expired', 'status')
        widgets = {
            'date_activity': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'readonly': True},
                                             format='%Y-%m-%d'),
            'keterangan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Activity/Action'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }


class ListActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ('activity2topik', 'activity2user', 'expired', 'status')
        widgets = {
            'date_activity': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'readonly': True},
                                             format='%Y-%m-%d'),
            'keterangan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Activity/Action'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }


class UpdateActivityForm(forms.ModelForm):
    class Meta:
        model = Activity
        fields = '__all__'
        exclude = ('activity2topik', 'activity2user', 'expired', 'status')
        widgets = {
            'date_activity': forms.DateInput(attrs={'class': 'form-control', 'type': 'date', 'readonly': True},
                                             format='%Y-%m-%d'),
            'keterangan': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Activity/Action'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }


class CreatePicaForm(forms.ModelForm):
    class Meta:
        model = Topik
        fields = '__all__'
        exclude = ('topik2meeting', 'expired', 'due_date', 'topik2user', 'status', 'topik2peserta')
        widgets = {
            'issued_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'topik2departemen': forms.Select(attrs={'class': 'form-control'}),
            'topik2company': forms.Select(attrs={'class': 'form-control'}),
            'nama_topik': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Topik'}, ),
            'problem': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Problem'}),
            'action': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Solution'}),
        }


class UpdatePicaForm(forms.ModelForm):
    class Meta:
        model = Topik
        fields = '__all__'
        exclude = ('topik2meeting', 'expired', 'topik2user', 'topik2peserta')
        widgets = {
            'issued_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}),
            'topik2departemen': forms.Select(attrs={'class': 'form-control'}),
            'topik2company': forms.Select(attrs={'class': 'form-control'}),
            'nama_topik': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama topik'}, ),
            'problem': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Problem'}),
            'action': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Solution'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }


class UpdatePicaActionForm(forms.ModelForm):
    class Meta:
        model = Topik
        fields = ('nama_topik', 'problem', 'action', 'due_date')
        widgets = {
            'nama_topik': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama topik'}, ),
            'problem': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Problem'}),
            'action': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Solution'}),
            'due_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
        }


class CreateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Code'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'})
        }


class UpdateCompanyForm(forms.ModelForm):
    class Meta:
        model = Company
        fields = "__all__"
        widgets = {
            'name': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Company Name'}),
            'description': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Description'})
        }


class CreatePesertaForm(forms.ModelForm):
    class Meta:
        model = Peserta
        fields = "__all__"
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama peserta'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'bod': forms.NullBooleanSelect(attrs={'class': 'form-control', 'placeholder': 'BOD?'}),
        }


class UpdateDashboardForm(forms.ModelForm):
    class Meta:
        model = Meeting
        fields = ("meeting_date", "start_time", "end_time")
        widgets = {
            'meeting_date': forms.DateInput(attrs={'class': 'form-control', 'type': 'date'}, format='%Y-%m-%d'),
            'start_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'),
            'end_time': forms.TimeInput(attrs={'class': 'form-control', 'type': 'time'}, format='%H:%M'),
        }


class UpdatePesertaForm(forms.ModelForm):
    class Meta:
        model = Peserta
        fields = "__all__"
        widgets = {
            'nama': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nama peserta'}),
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Email address'}),
            'bod': forms.NullBooleanSelect(attrs={'class': 'form-control', 'placeholder': 'BOD?'}),
        }
