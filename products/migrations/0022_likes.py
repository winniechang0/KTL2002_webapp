# Generated by Django 3.1.3 on 2021-04-11 10:57

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0021_delete_likes'),
    ]

    operations = [
        migrations.CreateModel(
            name='Likes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('Like', models.IntegerField(default=0)),
                ('Like_date', models.DateField()),
                ('Offer', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='products.offer')),
                ('User', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
