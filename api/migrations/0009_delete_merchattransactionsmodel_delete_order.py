# Generated by Django 4.1.5 on 2023-02-16 11:10

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0008_merchattransactionsmodel_order'),
    ]

    operations = [
        migrations.DeleteModel(
            name='MerchatTransactionsModel',
        ),
        migrations.DeleteModel(
            name='Order',
        ),
    ]
