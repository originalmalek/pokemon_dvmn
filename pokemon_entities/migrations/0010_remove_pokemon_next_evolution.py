# Generated by Django 4.1.7 on 2023-02-28 16:49

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('pokemon_entities', '0009_alter_pokemon_next_evolution_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='pokemon',
            name='next_evolution',
        ),
    ]
