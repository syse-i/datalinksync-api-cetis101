# Generated by Django 4.1.7 on 2023-04-04 15:55

from django.db import migrations
import django.utils.timezone
import django_extensions.db.fields


class Migration(migrations.Migration):

    dependencies = [
        ('sync', '0002_synccontent_sync_syncco_content_42caac_idx'),
    ]

    operations = [
        migrations.AddField(
            model_name='synccontent',
            name='created',
            field=django_extensions.db.fields.CreationDateTimeField(auto_now_add=True, default=django.utils.timezone.now, verbose_name='created'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='synccontent',
            name='modified',
            field=django_extensions.db.fields.ModificationDateTimeField(auto_now=True, verbose_name='modified'),
        ),
    ]
