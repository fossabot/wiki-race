# Generated by Django 3.2.9 on 2021-11-27 15:34

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('wiki_app', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='round',
            name='running',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='round',
            name='start_time',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AlterField(
            model_name='memberround',
            name='round',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='member_rounds', to='wiki_app.round'),
        ),
    ]
