import folium
import json

from django.http import HttpResponseNotFound
from django.shortcuts import render
from django.utils.timezone import localtime

from .models import PokemonEntity, Pokemon


MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
    'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
    '/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
    '&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url=DEFAULT_IMAGE_URL):
    icon = folium.features.CustomIcon(
        image_url,
        icon_size=(50, 50),
    )
    folium.Marker(
        [lat, lon],
        # Warning! `tooltip` attribute is disabled intentionally
        # to fix strange folium cyrillic encoding bug
        icon=icon,
    ).add_to(folium_map)


def show_all_pokemons(request):
    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    pokemons = Pokemon.objects.all()

    pokemons_on_page = []
    for pokemon in pokemons:
        pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon.id,
                                                        appeared_at__lt=localtime(),
                                                        disappeared_at__gt=localtime())
        for pokemon_entity in pokemon_entities:
            latitude = pokemon_entity.lat
            longitude = pokemon_entity.lon
            image_url = request.build_absolute_uri(pokemon_entity.pokemon.picture.url)

            add_pokemon(folium_map, latitude, longitude, image_url)

        pokemons_on_page.append({
            'pokemon_id': pokemon.id,
            'img_url': request.build_absolute_uri(pokemon.picture.url),
            'title_ru': pokemon.title,
        })
   
    return render(request, 'mainpage.html', context={
        'map': folium_map._repr_html_(),
        'pokemons': pokemons_on_page,
    })


def show_pokemon(request, pokemon_id):
    try:
        pokemon = Pokemon.objects.get(id=pokemon_id)
    except Pokemon.DoesNotExist:
        return HttpResponseNotFound('<h1>Такой покемон не найден</h1>')

    pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon_id,
                                                 appeared_at__lt=localtime(),
                                                 disappeared_at__gt=localtime())

    folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
    for pokemon_entity in pokemon_entities:
        latitude = pokemon_entity.lat
        longitude = pokemon_entity.lon
        image_url = request.build_absolute_uri(pokemon_entity.pokemon.picture.url)

        add_pokemon(folium_map, latitude, longitude, image_url)

    pokemon = {"pokemon_id": pokemon_id,
        "title_ru": pokemon.title,
        "title_en": "Venusaur",
        "title_jp": "フシギバナ",
        "description": "покемон двойного травяного и ядовитого типа из первого поколения покемонов. На 32 уровне эволюционирует из Ивизавра. Финальная эволюция травяного стартовика Бульбазавра. Развивается в Мега Венузавра с помощью камня Венусарита.",
        "img_url": request.build_absolute_uri(pokemon.picture.url),

    }

    return render(request, 'pokemon.html', context={
        'map': folium_map._repr_html_(), 'pokemon': pokemon
    })
