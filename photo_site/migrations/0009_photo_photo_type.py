# Generated by Django 4.2 on 2023-05-25 13:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('photo_site', '0008_alter_lens_name'),
    ]

    operations = [
        migrations.AddField(
            model_name='photo',
            name='photo_type',
            field=models.CharField(choices=[('landscape', 'Landscape'), ('street', 'Street'), ('macro', 'Macro'), ('astro', 'Astrophotography'), ('portrait', 'Portrait'), ('night', 'Night'), ('bw', 'Black & White'), ('travel', 'Travel'), ('abstract', 'Abstract'), ('experimental', 'Experimental'), ('fashion', 'Fashion'), ('long exposure', 'Long Exposure'), ('aerial', 'Aerial'), ('product', 'Product'), ('advertising', 'Advertising'), ('wedding', 'Wedding'), ('sports', 'Sports'), ('still life', 'Still Life'), ('photojournalism', 'Photojournalism')], default='landscape', max_length=75),
        ),
    ]
