# Generated by Django 4.2.16 on 2024-10-08 17:07

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0015_alter_customer_options_remove_customer_email_and_more'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='order',
            options={'permissions': [('cancel_order', 'Can cancel order')]},
        ),
    ]
