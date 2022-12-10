from django.shortcuts import render
from django.http import HttpResponse
from anggaran.forms import AnggaranForm
from anggaran.models import Anggaran
from kategori.models import Kategori
from users.views import *
from django.contrib.auth.decorators import login_required, user_passes_test
from django.urls import reverse
from django.http import HttpResponseRedirect
from django.contrib import messages
import datetime

@login_required(login_url='/login/')
@user_passes_test(check_role_pencatat)
def index(request):
    delete_expired_anggaran(request)

    today = datetime.datetime.now()
    anggarans = Anggaran.objects.filter(user=request.user, tanggal_mulai__gte=today)
    response = {'anggarans': anggarans}

    return render(request, 'anggaran_index.html', response)

@login_required(login_url='/login/')
@user_passes_test(check_role_pencatat)
def buat_anggaran(request):
    context = {}
  
    form = AnggaranForm(request.POST or None)
    form.fields['kategori'].queryset = Kategori.objects.filter(user=request.user, jenis_kategori=2)

    if form.is_valid() and request.method == 'POST':
        anggaran_form = form.save(commit=False)
        anggaran_form.user = request.user
        anggaran_form.save()
        messages.success(request, 'Anggaran baru berhasil dibuat!')
        return HttpResponseRedirect(reverse('anggaran:index'))

    elif form.errors:

        for error in form.errors:

            if (error == 'tanggal_mulai') or (error == 'tanggal_selesai'):
                messages.error(request, 'Tanggal yang dimasukkan tidak boleh lampau!')
            
            elif error == 'kategori':
                messages.error(request, 'Anggaran dengan kategori ini sudah pernah dibuat dan masih berjalan!')

    context['form'] = form
    return render(request, "buat_anggaran.html", context)

def delete_expired_anggaran(request):
    today = datetime.datetime.now()
    expired_anggarans = Anggaran.objects.filter(user=request.user, tanggal_mulai__lt=today)
    for  anggaran in expired_anggarans:
        anggaran.delete()
