# Generated by Django 2.0.3 on 2018-10-18 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pedidos', '0003_auto_20181007_2344'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='monto',
            field=models.FloatField(default=0, verbose_name='Costo de Pedido'),
        ),
    ]