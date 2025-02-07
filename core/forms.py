from django import forms
from .models import Shartnoma

class ShartnomaForm(forms.ModelForm):
    class Meta:
        model = Shartnoma
        fields = '__all__'

        widgets = {
            # ForeignKey fields
            'client': forms.Select(attrs={'class': 'form-control select2', 'placeholder': 'Наименование заказчика'}),
            'client_product': forms.Select(
                attrs={'class': 'form-control select2', 'placeholder': 'Наименование продукции'}),

            # CharField fields
            'ishlabchiqaruvchi': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Наименование изготовителя'}),
            'maqsad': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Цель, задачи и вид испытаний'}),
            'malumot': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Информация об отборе образцов'}),
            'nd_obyekt': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'НД на объекты испытания'}),
            'nd_metod': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'НД на методы испытания'}),
            'sinov_shartlari': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Условия проведения испытаний'}),
            'qushimcha': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Дополнительная информация'}),
            'information': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Информация о субподрядных работах'}),
            'nd_talab_qiymat': forms.TextInput(
                attrs={'class': 'form-control', 'placeholder': 'Значения требования по НД'}),
            'fakt_qiymati': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Фактическое Значения'}),
            'unique_id': forms.TextInput(attrs={'class': 'form-control', 'readonly': 'readonly'}),  # Read-only field

            # ManyToManyField fields
            'ulchov_asbob': forms.SelectMultiple(attrs={'class': 'form-control select2'}),  # ManyToManyField
            'sertifikatlash': forms.SelectMultiple(attrs={'class': 'form-control select2'}),  # ManyToManyField
            'sklad': forms.SelectMultiple(attrs={'class': 'form-control select2'}),  # ManyToManyField
            'gost': forms.SelectMultiple(attrs={'class': 'form-control select2'}),  # ManyToManyField
            'parametr': forms.SelectMultiple(attrs={'class': 'form-control select2'}),  # ManyToManyField
            'tekshiruv_kurinishi': forms.SelectMultiple(attrs={'class': 'form-control select2'}),  # ManyToManyField            # DateField fields
            'qabul_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'YYYY-MM-DD'}),
            'protocol_date': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'YYYY-MM-DD'}),
            'sinov_sanasi': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'YYYY-MM-DD'}),
            'imzo_sanasi': forms.DateInput(attrs={'class': 'form-control datepicker', 'placeholder': 'YYYY-MM-DD'}),
            # ImageField for QR Code
            'qr_code': forms.ClearableFileInput(attrs={'class': 'form-control-file'}),
        }