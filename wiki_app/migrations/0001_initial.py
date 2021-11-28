# Generated by Django 3.2.9 on 2021-11-27 12:06

import django.contrib.postgres.fields
from django.db import migrations, models
import django.db.models.deletion
import uuid


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Party',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
                ('time_limit', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('uid', models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True, serialize=False)),
            ],
        ),
        migrations.CreateModel(
            name='Round',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_page', models.CharField(max_length=100)),
                ('end_page', models.CharField(max_length=100)),
                ('solution', django.contrib.postgres.fields.ArrayField(base_field=models.CharField(max_length=100), size=None)),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='wiki_app.party')),
            ],
        ),
        migrations.CreateModel(
            name='PartyMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('points', models.IntegerField(default=0)),
                ('party', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='wiki_app.party')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wiki_app.user')),
            ],
        ),
        migrations.CreateModel(
            name='MemberRound',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('current_page', models.CharField(max_length=100)),
                ('solved_at', models.IntegerField(default=-1)),
                ('member', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='rounds', to='wiki_app.partymember')),
                ('round', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='wiki_app.round')),
            ],
        ),
        migrations.CreateModel(
            name='AdminRole',
            fields=[
                ('party', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, primary_key=True, serialize=False, to='wiki_app.party')),
                ('admin_member', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='wiki_app.partymember')),
            ],
        ),
    ]
