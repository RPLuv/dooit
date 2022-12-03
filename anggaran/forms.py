from django import forms
from django.forms import widgets
from .models import Anggaran

class AnggaranForm(forms.ModelForm):
    class Meta:
        model = Anggaran
        fields = ['nominal', 'deskripsi', 'kategori', 'tanggal_mulai', 'tanggal_selesai']

        widgets = {
                    'tanggal_mulai': forms.DateInput(
                        format=('%Y-%m-%d'),
                        attrs={'class': 'form-control', 
                            'placeholder': 'Select a date',
                            'type': 'date'
                            }),

                    'tanggal_selesai': forms.DateInput(
                        format=('%Y-%m-%d'),
                        attrs={'class': 'form-control', 
                            'placeholder': 'Select a date',
                            'type': 'date'
                            })
        }