# Generated by Django 4.2.1 on 2023-06-03 23:00

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='recipe',
            name='author',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='ingredients',
        ),
        migrations.RemoveField(
            model_name='recipe',
            name='tags',
        ),
        migrations.RemoveField(
            model_name='recipeingredients',
            name='ingredient',
        ),
        migrations.RemoveField(
            model_name='recipeingredients',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='recipetags',
            name='recipe',
        ),
        migrations.RemoveField(
            model_name='recipetags',
            name='tag',
        ),
        migrations.DeleteModel(
            name='Follow',
        ),
        migrations.DeleteModel(
            name='Ingredients',
        ),
        migrations.DeleteModel(
            name='Recipe',
        ),
        migrations.DeleteModel(
            name='RecipeIngredients',
        ),
        migrations.DeleteModel(
            name='RecipeTags',
        ),
        migrations.DeleteModel(
            name='Tags',
        ),
    ]