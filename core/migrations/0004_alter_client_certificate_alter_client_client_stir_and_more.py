# Generated by Django 5.1.4 on 2025-02-06 04:28

import django.core.validators
import uuid
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0003_alter_client_options_alter_clientproduct_options_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='client',
            name='certificate',
            field=models.FileField(upload_to='guvohnomalar/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png'])], verbose_name='Guvohnoma'),
        ),
        migrations.AlterField(
            model_name='client',
            name='client_stir',
            field=models.CharField(max_length=15, verbose_name='Stir kodi'),
        ),
        migrations.AlterField(
            model_name='client',
            name='id',
            field=models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False),
        ),
        migrations.AlterField(
            model_name='client',
            name='mfo',
            field=models.CharField(max_length=10, verbose_name='MFO'),
        ),
        migrations.AlterField(
            model_name='client',
            name='passport_file',
            field=models.FileField(upload_to='client-passports/', validators=[django.core.validators.FileExtensionValidator(allowed_extensions=['pdf', 'jpg', 'png'])], verbose_name='Passport file'),
        ),
        migrations.AlterField(
            model_name='client',
            name='schot_number',
            field=models.CharField(max_length=20, verbose_name='Hisob raqami'),
        ),
    ]
