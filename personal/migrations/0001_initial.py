# Generated by Django 2.0 on 2018-10-01 20:40

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Conductor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('cedula', models.IntegerField(unique=True, verbose_name='Cedula de Identidad')),
                ('phone', models.IntegerField(verbose_name='Telefono de Referencia')),
                ('ciudad', models.CharField(max_length=20, verbose_name='Ciudad de Origen')),
                ('nro_licencia', models.CharField(max_length=20, verbose_name='Numero de Licencia')),
                ('categoria', models.CharField(max_length=10, verbose_name='Categoria Licencia')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Conductor',
                'verbose_name_plural': 'Conductores',
                'ordering': ['cedula'],
            },
        ),
    ]
