# Generated by Django 2.2.6 on 2019-11-14 07:14

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('mobilestore', '0004_auto_20191114_0713'),
    ]

    operations = [
        migrations.AlterField(
            model_name='productcategory',
            name='parent',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.CASCADE, to='mobilestore.ProductCategory'),
        ),
    ]