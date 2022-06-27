# Generated by Django 4.0.5 on 2022-06-27 10:08

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_email', models.CharField(max_length=100)),
                ('product_name', models.CharField(max_length=100)),
                ('order_amount', models.CharField(max_length=25)),
                ('isPaid', models.BooleanField(default=False)),
                ('order_date', models.DateTimeField(auto_now=True)),
            ],
        ),
    ]