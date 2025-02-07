from django.shortcuts import render
from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, UpdateView, DeleteView, CreateView
from .models import Client, ClientProduct, Sklad, GostParametr, Gost, Shartnoma
# from .serializers import *
from django.urls import reverse_lazy
# from .forms import *
from django.http import HttpResponse
from django.shortcuts import redirect
from django.http import JsonResponse
from django.views.generic import View
# Create your views here.
class ShartnomaDetailView(View):
    template_name = 'admin/shartnoma_detail.html'

    def get(self, request, unique_id):
        shartnoma = get_object_or_404(Shartnoma, unique_id=unique_id)

        # Har bir o'lchov asbobi uchun unga tegishli sertifikatlarni ro'yxatlash
        asboblar = shartnoma.ulchov_asbob.all()  # barcha ulchov asboblarni olish
        asbob_sertifikatlari = []
        for asbob in asboblar:
            sertifikatlar = shartnoma.sertifikatlash.filter(id=asbob.id)  # bog'langan sertifikatlarni filtrlash
            asbob_sertifikatlari.append({
                'asbob': asbob,
                'sertifikatlar': sertifikatlar
            })

        # Templatega yuborish
        return render(
            request,
            self.template_name,
            {'shartnoma': shartnoma, 'asbob_sertifikatlari': asbob_sertifikatlari}
        )
from django.shortcuts import render, redirect
from .forms import ShartnomaForm


def add_shartnoma(request):
    if request.method == 'POST':
        form = ShartnomaForm(request.POST, request.FILES)  # Fayllar yuklash uchun `FILES`
        if form.is_valid():
            form.save()
            return redirect('shartnoma_success')  # Ma'lumot qo'shilgandan keyin boshqa sahifaga o'tish
    else:
        form = ShartnomaForm()
    return render(request, 'shartnoma_form.html', {'form': form})


def shartnoma_success(request):
    return render(request, 'shartnoma_success.html')
