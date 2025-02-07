# Generated by Django 5.1.3 on 2024-11-24 09:18

import django.db.models.deletion
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Client',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('client_name', models.CharField(max_length=255, verbose_name='Mijoz nomi')),
                ('passport_file', models.FileField(upload_to='client-passports/', verbose_name='Passport file')),
                ('work_name', models.CharField(max_length=255, verbose_name='Ish faoliyati nomi')),
                ('direktor', models.CharField(max_length=255, verbose_name='Direktor ism familiyasi')),
                ('location', models.CharField(max_length=255, verbose_name='Yuridik manzil')),
                ('client_stir', models.IntegerField(verbose_name='Stir kodi')),
                ('mfo', models.IntegerField(verbose_name='MFO')),
                ('schot_number', models.IntegerField(verbose_name='Hisob raqami')),
                ('certificate', models.FileField(upload_to='guvohnomalar/', verbose_name='Guvohnoma')),
            ],
        ),
        migrations.CreateModel(
            name='GostParametr',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('parametr_name', models.CharField(max_length=250, verbose_name='Parametr nomi')),
            ],
        ),
        migrations.CreateModel(
            name='Sklad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('item_name', models.CharField(max_length=255, verbose_name='Tovar nomi')),
                ('manufacturer', models.CharField(max_length=255, verbose_name='Ishlab chiqaruvchi')),
                ('parametr', models.CharField(max_length=255, verbose_name='Paramaetrlari')),
                ('certificate', models.FileField(upload_to='certificate/')),
                ('birlik', models.CharField(choices=[('kg', 'kg'), ('gr', 'gr'), ('m2', 'm2'), ('mg', 'mg'), ('m3', 'm3')], max_length=10, verbose_name='Birligi')),
                ('quantity', models.IntegerField(verbose_name='Qiymati')),
                ('start_date', models.DateField(verbose_name='Ishlab chiqarilgan sana')),
                ('end_date', models.DateField(verbose_name='Tugash muddati')),
                ('add_date', models.DateField(auto_now=True)),
                ('status', models.BooleanField(default=True, verbose_name='Status')),
            ],
        ),
        migrations.CreateModel(
            name='ClientProduct',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('product', models.CharField(max_length=255, verbose_name='Maxsulot nomi')),
                ('product_quantity', models.IntegerField(verbose_name='Maxsulot qiymati')),
                ('product_unity', models.CharField(choices=[('kg', 'kg'), ('gr', 'gr'), ('m2', 'm2'), ('mg', 'mg'), ('m3', 'm3')], max_length=10, verbose_name='Birligi')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.client')),
            ],
        ),
        migrations.CreateModel(
            name='Gost',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('position_code', models.CharField(max_length=250, verbose_name='Pozitsiya kodi')),
                ('gost_name', models.CharField(max_length=250, verbose_name='Gost nomi')),
                ('test_gost', models.CharField(max_length=250, verbose_name='Briktirilgan test sinovi')),
                ('test_code', models.CharField(max_length=250, verbose_name='Test kodi')),
                ('parametr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gostparametr', verbose_name='Parametr nomi')),
            ],
        ),
        migrations.CreateModel(
            name='Shartnoma',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ishlabchiqaruvchi', models.CharField(max_length=255, verbose_name='Наименование изготовителя ')),
                ('maqsad', models.CharField(max_length=255, verbose_name='Цель, задачи и вид испытаний')),
                ('malumot', models.CharField(max_length=255, verbose_name='Информация об отборе образцов')),
                ('nd_obyekt', models.CharField(max_length=255, verbose_name='НД на объекты испытания')),
                ('nd_metod', models.CharField(max_length=255, verbose_name='НД на методы испытания')),
                ('sinov_shartlari', models.CharField(max_length=255, verbose_name='Условия проведения испытаний')),
                ('qabul_date', models.DateField(verbose_name='Дата получения образцов')),
                ('ulchov_asbob', models.CharField(max_length=255, verbose_name='Наименование средств измерений и испытательных оборудований:')),
                ('sertifikatlash', models.CharField(max_length=255, verbose_name='Сертификаты поверки/калибровки или аттестации')),
                ('protocol_date', models.DateField(verbose_name='Shartnoma tuzilgan vaqt')),
                ('qushimcha', models.CharField(max_length=255, verbose_name='Дополнительная информация')),
                ('information', models.CharField(max_length=255, verbose_name='Информация о субподрядных работах')),
                ('sinov_sanasi', models.DateField(verbose_name='Дата проведения испытания')),
                ('imzo_sanasi', models.DateField(verbose_name='Дата подписания протокола')),
                ('tekshiruv_kurinishi', models.CharField(max_length=255, verbose_name='Вид испытания')),
                ('nd_talab_qiymat', models.CharField(max_length=255, verbose_name='Значения требования по НД')),
                ('fakt_qiymati', models.CharField(max_length=255, verbose_name='Фактическое Значения')),
                ('unique_id', models.CharField(editable=False, max_length=9, unique=True)),
                ('qr_code', models.ImageField(blank=True, editable=False, null=True, upload_to='qr_codes/')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.client', verbose_name='Наименование заказчика')),
                ('client_product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.clientproduct', verbose_name='Наименование продукции')),
                ('gost', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gost', verbose_name='Gost')),
                ('parametr', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.gostparametr', verbose_name='Gost parametr')),
                ('sklad', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.sklad', verbose_name='Sklad')),
            ],
            options={
                'verbose_name': 'Shartnoma',
                'verbose_name_plural': 'Shartnoma',
            },
        ),
        migrations.CreateModel(
            name='Services',
            fields=[
                ('id', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('service_quantity', models.IntegerField(verbose_name='Xizmat qiymati')),
                ('client', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.client', verbose_name='Mijozlar')),
                ('product', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='core.sklad', verbose_name='Maxsulotlar')),
            ],
        ),
    ]
