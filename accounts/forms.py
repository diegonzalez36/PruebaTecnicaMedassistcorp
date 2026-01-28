from django import forms
from dbmedical.models import Visit, Doctor, Institution, VisitType
from datetime import datetime


class VisitForm(forms.ModelForm):
    visit_date = forms.DateTimeField(
        widget=forms.DateTimeInput(attrs={
            'type': 'datetime-local',
            'class': 'form-control'
        }),
        input_formats=['%Y-%m-%dT%H:%M']
    )
    
    class Meta:
        model = Visit
        fields = ['visit_type', 'status', 'gestor', 'doctor', 'institution', 
                  'visit_date', 'duration_minutes', 'objective', 'notes']
        widgets = {
            'visit_type': forms.Select(attrs={'class': 'form-control'}),
            'status': forms.Select(attrs={'class': 'form-control'}),
            'gestor': forms.Select(attrs={'class': 'form-control'}),
            'doctor': forms.Select(attrs={'class': 'form-control'}),
            'institution': forms.Select(attrs={'class': 'form-control'}),
            'duration_minutes': forms.NumberInput(attrs={'class': 'form-control', 'min': '15', 'step': '15'}),
            'objective': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
            'notes': forms.Textarea(attrs={'class': 'form-control', 'rows': 3}),
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hacer campos opcionales según tipo
        self.fields['doctor'].required = False
        self.fields['institution'].required = False
        self.fields['objective'].required = False
        self.fields['notes'].required = False
    
    def clean(self):
        cleaned_data = super().clean()
        visit_type = cleaned_data.get('visit_type')
        doctor = cleaned_data.get('doctor')
        institution = cleaned_data.get('institution')
        
        # Validar que según el tipo, tenga médico o institución
        if visit_type:
            if visit_type.name.lower() == 'médicos' and not doctor:
                raise forms.ValidationError('Debe seleccionar un médico para este tipo de visita.')
            if visit_type.name.lower() == 'instituciones' and not institution:
                raise forms.ValidationError('Debe seleccionar una institución para este tipo de visita.')
        
        return cleaned_data