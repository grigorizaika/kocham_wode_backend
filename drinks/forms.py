from django import forms


class StatisticsParametersForm(forms.Form):
    date = forms.DateField(required=False)
    date_start = forms.DateField(required=False)
    date_end = forms.DateField(required=False)

    def clean(self):
        d = self.cleaned_data.get('date', None)
        ds = self.cleaned_data.get('date_start', None)
        de = self.cleaned_data.get('date_end', None)

        if d and (ds or de):
            raise forms.ValidationError(
                "Please specify date OR date_start and date_end")

        if (ds and not de) or (de and not ds):
            raise forms.ValidationError(
                "Please specify date_start and date_end together")