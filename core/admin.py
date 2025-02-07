from django.contrib import admin
from .models import *
from django.utils.html import format_html
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.conf import settings
from django.db.models import Q
from django.contrib import messages

@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = (
        'client_name', 'work_name', 'direktor', 'location', 'client_stir',
        'mfo', 'schot_number', 'display_certificate', 'display_passport_file'
    )
    search_fields = ('client_name', 'work_name', 'direktor')
    list_filter = ('work_name', 'location')
    ordering = ('client_name',)
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        try:
            obj.clean()
            super().save_model(request, obj, form, change)
        except ValidationError as e:
            for field, errors in e.message_dict.items():
                for error in errors:
                    self.message_user(request, f"{field}: {error}", level=messages.ERROR)

    def display_certificate(self, obj):
        if obj.certificate:
            file_url = f"{settings.MEDIA_URL}{obj.certificate}"
            if file_url.lower().endswith(('png', 'jpg', 'jpeg')):
                return format_html(
                    '<a href="{}" download><img src="{}" width="100" height="100" /></a>',
                    file_url, file_url
                )
            else:
                return format_html('<a href="{}" download>{}</a>', file_url, "Yuklab olish")
        return "Fayl mavjud emas"

    display_certificate.short_description = 'Certificate'

    def display_passport_file(self, obj):
        if obj.passport_file:
            file_url = f"{settings.MEDIA_URL}{obj.passport_file}"
            if file_url.lower().endswith(('png', 'jpg', 'jpeg')):
                return format_html(
                    '<a href="{}" download><img src="{}" width="100" height="100" /></a>',
                    file_url, file_url
                )
            else:
                return format_html('<a href="{}" download>{}</a>', file_url, "Yuklab olish")
        return "Fayl mavjud emas"

    display_passport_file.short_description = 'Passport File'

@admin.register(ClientProduct)
class ClientProductAdmin(admin.ModelAdmin):
    list_display = ('client', 'product', 'product_quantity', 'product_unity')
    search_fields = ('client__client_name', 'product')
    list_filter = ('product_unity',)

    def save_model(self, request, obj, form, change):
        if obj.product_quantity <= 0:
            self.message_user(request, "Maxsulot qiymati 0 yoki 0 dan kichik bo'lishi mumkin emas.", level='error')
            return
        if obj.product_unity == "0":
            self.message_user(request, "Birligi 0 bo'lishi mumkin emas.", level='error')
            return

        obj.save()

@admin.register(Sklad)
class SkladAdmin(admin.ModelAdmin):
    list_display = (
        'display_name_with_expiry_highlight', 'manufacturer', 'parametr', 'display_full_quantity', 'start_date', 'end_date',
        'days_until_expiry', 'status', 'display_certificate', 'check_quantity_status'
    )
    search_fields = ('item_name', 'manufacturer')
    ordering = ('end_date', 'quantity')
    list_filter = ('manufacturer', 'status')
    list_per_page = 25

    def save_model(self, request, obj, form, change):
        # Mahsulotning nomi boshqa mahsulotlar bilan o'xshash bo'lsa
        if Sklad.objects.filter(item_name=obj.item_name).exists():
            self.message_user(request, "Bunday mahsulot mavjud.", level='error')
            return

        # Mahsulot qiymatini tekshirish
        if obj.quantity <= 0:
            self.message_user(request, "Mahsulot qiymati 0 yoki 0 dan kichik bo'lishi mumkin emas.", level='error')
            return

        super().save_model(request, obj, form, change)

    def display_certificate(self, obj):
        if obj.certificate:
            file_url = f"{obj.certificate.url}"

            if file_url.lower().endswith(('png', 'jpg', 'jpeg')):
                return format_html(
                    '<a href="{}" download><img src="{}" width="100" height="100" /></a>',
                    file_url, file_url
                )
            elif file_url.lower().endswith('pdf'):
                return format_html('<a href="{}" download>Yuklab olish (PDF)</a>', file_url)
            else:
                return format_html('<a href="{}" download>Yuklab olish (Fayl)</a>', file_url)
        return "Fayl mavjud emas"

    display_certificate.short_description = 'Certificate'

    def display_name_with_expiry_highlight(self, obj):
        if obj.end_date and (obj.end_date - timezone.now().date()).days <= 10:
            return format_html('<span style="color: red;">{}</span>', obj.item_name)
        return obj.item_name

    display_name_with_expiry_highlight.short_description = 'Mahsulot nomi'

    def check_quantity_status(self, obj):
        if 1 <= obj.quantity <= 10:
            return format_html('<span style="color: red; font-weight:bold;">Tugamoqda</span>')
        return obj.status

    check_quantity_status.short_description = 'Qoldiq'

    def days_until_expiry(self, obj):
        if obj.end_date:
            days_left = (obj.end_date - timezone.now().date()).days
            if days_left <= 10:
                color = 'red'
            elif days_left <= 20:
                color = 'orange'
            else:
                color = 'green'
            return format_html('<span style="color: {};">{} kun</span>', color, days_left)
        return "Muddati ko'rsatilmagan"

    days_until_expiry.short_description = 'Muddati tugashigacha'

    def display_full_quantity(self, obj):
        return f"{obj.quantity} {obj.birlik}"

    display_full_quantity.short_description = 'To\'liq qiymati'

@admin.register(GostParametr)
class GostParametrAdmin(admin.ModelAdmin):
    list_display = ('parametr_name',)
    search_fields = ('parametr_name',)

    def save_model(self, request, obj, form, change):
        if not change and GostParametr.objects.filter(parametr_name=obj.parametr_name).exists():
            self.message_user(request, f"Gost parametr '{obj.parametr_name}' allaqachon mavjud.", level='error')
        else:
            super().save_model(request, obj, form, change)
            if change:
                self.message_user(request, f"Gost parametr '{obj.parametr_name}' muvaffaqiyatli yangilandi.",
                                  level='success')
            else:
                self.message_user(request, f"Yangi gost parametr '{obj.parametr_name}' muvaffaqiyatli qo'shildi.",
                                  level='success')

@admin.register(Gost)
class GostAdmin(admin.ModelAdmin):
    list_display = ('position_code', 'parametr', 'gost_name', 'test_gost', 'test_code')
    search_fields = ('position_code', 'gost_name', 'test_code')
    list_filter = ('parametr',)

    def save_model(self, request, obj, form, change):
        if not change:
            # Yangi gost qo'shayotganda tekshiruv
            if Gost.objects.filter(
                    Q(position_code=obj.position_code) |
                    Q(gost_name=obj.gost_name) |
                    Q(test_code=obj.test_code)
            ).exists():
                self.message_user(request, "Bu gost parametr allaqachon ro'yxatda mavjud.", level='error')
                return
            else:
                super().save_model(request, obj, form, change)
                self.message_user(request, "Yangi gost muvaffaqiyatli qo'shildi.", level='success')
        else:
            # Eskisini yangilayotganda
            super().save_model(request, obj, form, change)
            self.message_user(request, "Gost muvaffaqiyatli yangilandi.", level='success')

@admin.register(Shartnoma)
class ShartnomaAdmin(admin.ModelAdmin):
    list_display = (
        'client', 'ishlabchiqaruvchi', 'maqsad', 'qabul_date', 'protocol_date', 'display_unique_id_link', 'display_qr_code'
    )
    search_fields = ('client__client_name', 'ishlabchiqaruvchi', 'unique_id')
    list_filter = ('qabul_date', 'protocol_date')

    def display_qr_code(self, obj):
        if obj.qr_code:
            return format_html('<img src="{}" width="100" height="100" />', obj.qr_code.url)
        return "Fayl mavjud emas"

    display_qr_code.short_description = 'QR Kode'

    def display_unique_id_link(self, obj):
        url = f"https://guliston.cipher-edu.uz/shartnoma/{obj.unique_id}"
        return format_html('<a href="{}" target="_blank">{}</a>', url, obj.unique_id)

    display_unique_id_link.short_description = 'Unique ID'

@admin.register(UlchovAsbob)
class UlchovAsbobAdmin(admin.ModelAdmin):
    list_display = ('name', 'ser')
    search_fields = ('name', 'ser')
    list_filter = ('name',)

@admin.register(TekshiruvKurinishi)
class TekshiruvKurinishiAdmin(admin.ModelAdmin):
    list_display = ('name', 'measure', 'ammount')
    search_fields = ('name',)
    list_filter = ('measure',)

@admin.register(Services)
class ServicesAdmin(admin.ModelAdmin):
    list_display = ('id', 'client', 'product', 'display_full_service_quantity')
    search_fields = ('client__client_name', 'product__item_name')
    list_filter = ('product', 'value')
    ordering = ('client', 'product')
    list_per_page = 25

    def display_full_service_quantity(self, obj):
        return f"{obj.service_quantity} {obj.value}"

    display_full_service_quantity.short_description = 'Xizmat qiymati'