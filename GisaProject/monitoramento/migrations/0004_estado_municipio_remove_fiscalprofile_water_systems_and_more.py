# Generated by Django 4.2.19 on 2025-02-26 12:05

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('monitoramento', '0003_measurement_mac_address_alter_measurement_frequencia_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='Estado',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('sigla', models.CharField(max_length=2)),
            ],
        ),
        migrations.CreateModel(
            name='Municipio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('estado', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='municipios', to='monitoramento.estado')),
            ],
        ),
        migrations.RemoveField(
            model_name='fiscalprofile',
            name='water_systems',
        ),
        migrations.AlterField(
            model_name='fiscalprofile',
            name='user',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, related_name='fiscal_profile', to=settings.AUTH_USER_MODEL),
        ),
        migrations.CreateModel(
            name='SistemaAbastecimento',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField(blank=True, null=True)),
                ('municipio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sistemas', to='monitoramento.municipio')),
            ],
        ),
        migrations.AddField(
            model_name='fiscalprofile',
            name='sistema',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='fiscais', to='monitoramento.sistemaabastecimento'),
            preserve_default=False,
        ),
    ]
