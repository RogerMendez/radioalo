# Generated by Django 2.0.3 on 2018-10-14 13:54

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('pedidos', '0003_auto_20181007_2344'),
    ]

    operations = [
        migrations.CreateModel(
            name='Origen',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('latitud', models.FloatField()),
                ('longitud', models.FloatField()),
                ('fecha', models.DateField(auto_now_add=True)),
                ('hora', models.TimeField(auto_now_add=True)),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, to='pedidos.Pedido')),
            ],
            options={
                'verbose_name': '_Ubicacion de Origen',
                'verbose_name_plural': '_Ubicaciones de Origen',
                'ordering': ['pedido', 'fecha', 'hora'],
            },
        ),
    ]
