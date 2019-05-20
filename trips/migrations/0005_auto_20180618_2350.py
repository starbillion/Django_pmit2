# Generated by Django 2.0.6 on 2018-06-18 23:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('trips', '0004_roomtype_order'),
    ]

    operations = [
        migrations.AddField(
            model_name='trip',
            name='savings',
            field=models.IntegerField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='trip',
            name='current_price',
            field=models.IntegerField(),
        ),
        migrations.AlterField(
            model_name='trip',
            name='original_price',
            field=models.IntegerField(),
        ),
    ]