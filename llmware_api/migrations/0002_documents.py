# Generated by Django 5.0.3 on 2024-03-24 06:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('llmware_api', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='documents',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('doc', models.FileField(upload_to='docs/')),
                ('selected', models.BooleanField(default=True)),
            ],
        ),
    ]
