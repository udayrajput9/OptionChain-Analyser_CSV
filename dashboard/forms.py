from django import forms
from .models import MarketContext

class MarketContextForm(forms.ModelForm):
    class Meta:
        model = MarketContext
        fields = '__all__'
        widgets = {
            'date': forms.DateInput(attrs={'type': 'date'}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field_name in self.fields:
            css_class = 'form-control'
            if isinstance(self.fields[field_name].widget, forms.Select):
                css_class = 'form-select'
            self.fields[field_name].widget.attrs['class'] = css_class
            if field_name not in ['date', 'stock_symbol', 'context_slot']:
                self.fields[field_name].required = False

    def clean(self):
        cleaned_data = super().clean()
        stock_symbol = (cleaned_data.get('stock_symbol') or '').strip().upper()
        cleaned_data['stock_symbol'] = stock_symbol
        for field_name in self.fields:
            if field_name not in ['date', 'stock_symbol', 'context_slot', 'us_market_sentiment', 'overall_market_sentiment', 'analyst_notes']:
                if cleaned_data.get(field_name) is None:
                    cleaned_data[field_name] = 0
            elif field_name == 'us_market_sentiment' and not cleaned_data.get(field_name):
                cleaned_data[field_name] = 'NEUTRAL'
        return cleaned_data


class OptionChainUploadForm(forms.Form):
    stock_symbol = forms.CharField(max_length=20)
    csv_file = forms.FileField()

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['stock_symbol'].widget.attrs['class'] = 'form-control'
        self.fields['csv_file'].widget.attrs['class'] = 'form-control'

    def clean_stock_symbol(self):
        return self.cleaned_data['stock_symbol'].strip().upper()

    def clean_csv_file(self):
        csv_file = self.cleaned_data['csv_file']
        if not csv_file.name.lower().endswith('.csv'):
            raise forms.ValidationError("Sirf CSV file upload karo.")
        return csv_file
