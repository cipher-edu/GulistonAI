from django.db import models
import uuid
from datetime import date, timedelta
import random
import string
import qrcode
import os
import qrcode
import string
import random
from io import BytesIO
from django.core.files import File
from django.core.validators import FileExtensionValidator
from django.core.exceptions import ValidationError
from datetime import date, timedelta

Birliklar = (
    ("kg", "kg"),
    ("gr", "gr"),
    ("m2", "m2"),
    ("mg", "mg"),
    ("m3", "m3"),
)

class Client(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client_name = models.CharField(max_length=255, verbose_name='Mijoz nomi')
    passport_file = models.FileField(upload_to='client-passports/', verbose_name='Passport file', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png'])])
    work_name = models.CharField(max_length=255, verbose_name='Ish faoliyati nomi')
    direktor = models.CharField(max_length=255, verbose_name='Direktor ism familiyasi')
    location = models.CharField(max_length=255, verbose_name='Yuridik manzil')
    client_stir = models.CharField(max_length=15, verbose_name='Stir kodi')
    mfo = models.CharField(max_length=10, verbose_name='MFO')
    schot_number = models.CharField(max_length=20, verbose_name='Hisob raqami')
    certificate = models.FileField(upload_to='guvohnomalar/', verbose_name='Guvohnoma', validators=[FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png'])])

    def clean(self):
        allowed_extensions = ['pdf', 'jpg', 'png']
        if self.certificate and not self.certificate.name.split('.')[-1].lower() in allowed_extensions:
            raise ValidationError({'certificate': 'Noto\'g\'ri fayl formati. Faqat pdf, jpg, png formatlar qabul qilinadi.'})
        if self.passport_file and not self.passport_file.name.split('.')[-1].lower() in allowed_extensions:
            raise ValidationError({'passport_file': 'Noto\'g\'ri fayl formati. Faqat pdf, jpg, png formatlar qabul qilinadi.'})

    def __str__(self):
        return self.client_name

    class Meta:
        verbose_name = 'Mijoz qo\'shish'
        verbose_name_plural = 'Mijozlarni qo\'shish'

class Sklad(models.Model):
    item_name = models.CharField(max_length=255, verbose_name='Tovar nomi')
    manufacturer = models.CharField(max_length=255, verbose_name='Ishlab chiqaruvchi')
    parametr = models.CharField(max_length=255, verbose_name='Paramaetrlari')
    certificate = models.FileField(upload_to='certificate/')
    birlik = models.CharField(max_length=10, choices=Birliklar, verbose_name='Birligi')
    quantity = models.IntegerField(verbose_name='Qiymati')
    start_date = models.DateField(verbose_name='Ishlab chiqarilgan sana', auto_now=False)
    end_date = models.DateField(verbose_name='Tugash muddati', auto_now=False)
    add_date = models.DateField(auto_now=True)
    status = models.BooleanField(default=True, verbose_name='Status')

    def __str__(self):
        return self.item_name

    def save(self, *args, **kwargs):
        if self.end_date < date.today():
            self.status = False
        elif self.end_date <= date.today() + timedelta(days=7):
            self.status = False

        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Ombor'
        verbose_name_plural = 'Omborxona'

class Services(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Mijozlar')
    product = models.ForeignKey(Sklad, on_delete=models.CASCADE, verbose_name='Maxsulotlar')
    service_quantity = models.IntegerField(verbose_name='Xizmat qiymati')
    value = models.CharField(max_length=50, verbose_name='Qiymatni tanlang', choices=[('kg', 'Kilogram'), ('gr', 'Gram'), ('m2', 'Square Meter'), ('mg', 'Milligram'), ('m3', 'Cubic Meter')])

    def save(self, *args, **kwargs):
        # Ensure the UUID is correctly formatted
        if not self.id or not isinstance(self.id, uuid.UUID):
            self.id = uuid.uuid4()
        
        # Subtract the service quantity from the selected product's quantity
        if self.product.birlik == 'kg' and self.value == 'gr':
            self.product.quantity -= self.service_quantity / 1000
        elif self.product.birlik == 'gr' and self.value == 'kg':
            self.product.quantity -= self.service_quantity * 1000
        elif self.product.birlik == 'm2' and self.value == 'm2':
            self.product.quantity -= self.service_quantity
        elif self.product.birlik == 'mg' and self.value == 'kg':
            self.product.quantity -= self.service_quantity * 1000000
        elif self.product.birlik == 'kg' and self.value == 'mg':
            self.product.quantity -= self.service_quantity / 1000000
        elif self.product.birlik == 'm3' and self.value == 'm3':
            self.product.quantity -= self.service_quantity
        else:
            self.product.quantity -= self.service_quantity
        
        self.product.save()
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.client.client_name} - {self.product.item_name} - {self.service_quantity}"

    class Meta:
        verbose_name = 'Servis'
        verbose_name_plural = 'Servis xizmatlar'

class ClientProduct(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    product = models.CharField(max_length=255, verbose_name='Maxsulot nomi')
    product_quantity = models.IntegerField(verbose_name='Maxsulot qiymati')
    product_unity = models.CharField(max_length=10, choices=Birliklar, verbose_name='Birligi')

    def __str__(self):
        return self.product

    class Meta:
        verbose_name = 'Mijoz maxsulotlari'
        verbose_name_plural = 'Mijozlar maxsuloti'



class GostParametr(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    parametr_name = models.CharField(verbose_name='Parametr nomi', max_length=250)

    def __str__(self):
        return self.parametr_name

    class Meta:
        verbose_name = 'Gost parametrlari'
        verbose_name_plural = 'Gost parametrlari'

class Gost(models.Model):
    # id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    position_code = models.CharField(verbose_name='Pozitsiya kodi', max_length=250)
    parametr = models.ForeignKey(GostParametr, on_delete=models.CASCADE, verbose_name='Parametr nomi')
    gost_name = models.CharField(verbose_name='Gost nomi', max_length=250)
    test_gost = models.CharField(verbose_name='Briktirilgan test sinovi', max_length=250)
    test_code = models.CharField(verbose_name='Test kodi', max_length=250)

    def __str__(self):
        return self.position_code

    class Meta:
        verbose_name = 'Gost'
        verbose_name_plural = 'Gostlar'

class UlchovAsbob(models.Model):
    name = models.CharField(max_length=255, verbose_name='Наименование средств измерений и испытательных оборудований:')
    ser = models.CharField(
        max_length=255,
        verbose_name='Наименование средств измерений и испытательных оборудований: Сертификаты поверки/калибровки или аттестации'
    )

    def __str__(self):
        return f"{self.name} / {self.ser}"

    class Meta:
        verbose_name = "O'lchov asboblari / sertifikatlari"
        verbose_name_plural = "O'lchov asboblari / sertifikatlari"

class TekshiruvKurinishi(models.Model):
    name = models.CharField(max_length=255, verbose_name='Вид испытания')
    measure = models.CharField(max_length=10, choices=Birliklar, verbose_name='Единица измерения')
    ammount = models.CharField(max_length=255, verbose_name='Количество')

    def __str__(self):
        return f"{self.name} / {self.measure} / {self.ammount}"

    class Meta:
        verbose_name = 'Вид испытания'
        verbose_name_plural = 'Виды испытания'

    class Meta:
        verbose_name = 'Tekshiruv'
        verbose_name_plural = 'Tekshiruv ko\'rinishlari'

class Shartnoma(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='Наименование заказчика')
    ishlabchiqaruvchi = models.CharField(max_length=255, verbose_name='Наименование изготовителя ')
    maqsad = models.CharField(verbose_name='Цель, задачи и вид испытаний', max_length=255)
    malumot = models.CharField(verbose_name='Информация об отборе образцов', max_length=255)
    client_product = models.ForeignKey(ClientProduct, on_delete=models.CASCADE, verbose_name='Наименование продукции')
    nd_obyekt = models.CharField(max_length=255, verbose_name='НД на объекты испытания')
    nd_metod = models.CharField(max_length=255, verbose_name='НД на методы испытания')
    sinov_shartlari = models.CharField(verbose_name='Условия проведения испытаний', max_length=255)
    qabul_date = models.DateField(auto_now=False, verbose_name='Дата получения образцов')
    ulchov_asbob = models.ManyToManyField(UlchovAsbob, related_name="shartnoma_ulchov_asbob",
                                          verbose_name='Наименование средств измерений и испытательных оборудований:')
    sertifikatlash = models.ManyToManyField(UlchovAsbob, related_name="shartnoma_sertifikatlash",
                                            verbose_name='Сертификаты поверки/калибровки или аттестации')
    sklad = models.ManyToManyField(Sklad, verbose_name='Sklad')
    gost = models.ManyToManyField(Gost, verbose_name='Gost')
    parametr = models.ManyToManyField(GostParametr, verbose_name='Gost parametr')
    protocol_date = models.DateField(auto_now=False, verbose_name='Shartnoma tuzilgan vaqt')
    qushimcha = models.CharField(verbose_name='Дополнительная информация', max_length=255)
    information = models.CharField(verbose_name='Информация о субподрядных работах', max_length=255)
    sinov_sanasi = models.DateField(auto_now=False, verbose_name='Дата проведения испытания')
    imzo_sanasi = models.DateField(auto_now=False, verbose_name='Дата подписания протокола')
    tekshiruv_kurinishi = models.ManyToManyField(TekshiruvKurinishi, verbose_name='Вид испытания')
    nd_talab_qiymat = models.CharField(verbose_name='Значения требования по НД', max_length=255)
    fakt_qiymati = models.CharField(verbose_name='Фактическое Значения', max_length=255)
    unique_id = models.CharField(max_length=9, unique=True, editable=False)
    qr_code = models.ImageField(upload_to='qr_codes/', editable=False, blank=True, null=True)

    def save(self, *args, **kwargs):
        if not self.unique_id:
            self.unique_id = self.generate_unique_id()
        super().save(*args, **kwargs)
        if not self.qr_code:
            self.generate_qr_code()
            super().save(*args, **kwargs)

    def generate_unique_id(self):
        characters = string.ascii_lowercase + string.digits
        while True:
            unique_id = ''.join(random.choices(characters, k=9))
            if not Shartnoma.objects.filter(unique_id=unique_id).exists():
                return unique_id


    def generate_qr_code(self):
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(self.unique_id)
        qr.make(fit=True)

        img = qr.make_image(fill='black', back_color='white')
        buffer = BytesIO()
        img.save(buffer, format="PNG")
        file_name = f'{self.unique_id}_qr.png'
        self.qr_code.save(file_name, File(buffer), save=False)

    class Meta:
        verbose_name = 'Shartnoma'
        verbose_name_plural = 'Shartnomalar'


#
# class News(models.Model):
#     id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#     title = models.CharField(max_length=255, verbose_name='Sarlavha')
#     about = models.TextField(verbose_name='Batafsil')
#     image = models.ImageField(upload_to='posts/', verbose_name='Surat')
#     date = models.DateField(auto_now=False)
#
#     def __str__(self):
#         return self.title
