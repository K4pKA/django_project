# Generated by Django 4.0 on 2021-12-21 17:30

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
        ('quests', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='IsPassedTest',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('IsPassed', models.BooleanField(default=False, verbose_name='Пройден ли тест')),
                ('TestID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='quests.profiletest', verbose_name='Тест')),
                ('UserID', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='auth.user', verbose_name='Пользователь')),
            ],
        ),
    ]