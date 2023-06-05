# Generated by Django 4.2.1 on 2023-06-04 23:27

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('recipe', '0006_remove_ingredients_amount_recipeingredients_amount'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('shopcart', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='shopcart',
            name='recipe',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='shopcart', to='recipe.recipe'),
        ),
        migrations.AlterField(
            model_name='shopcart',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
