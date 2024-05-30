import requests
from django import forms
from django.core.exceptions import ValidationError

from unique_content.models import FigureFromP3din, FigureThinSection
from users.forms import StyleFormMixin


class FigureFromP3dinForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = FigureFromP3din
        fields = ('title', 'description', 'preview', 'link',)

    def clean(self):
        cleaned_data = super().clean()
        figure_3d = cleaned_data.get('link')

        # Checking the correctness of the link to the p3d.in service
        if figure_3d:
            response = requests.get(figure_3d)
            status_code = response.status_code
            if not (figure_3d[0:15] == 'https://p3d.in/' and status_code == 200):
                self.add_error('figure_3d', 'Invalid p3d.in link')
                raise ValidationError("Invalid p3d.in link")

        return cleaned_data


class FigureThinSectionForm(StyleFormMixin, forms.ModelForm):
    class Meta:
        model = FigureThinSection
        fields = ('title', 'description', 'preview', 'file_ppl', 'file_cpl',)
