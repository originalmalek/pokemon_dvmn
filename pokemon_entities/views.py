import folium
from django.http import HttpResponseNotFound
from django.shortcuts import render, get_object_or_404
from django.utils.timezone import localtime

from .models import PokemonEntity, Pokemon

MOSCOW_CENTER = [55.751244, 37.618423]
DEFAULT_IMAGE_URL = (
	'https://vignette.wikia.nocookie.net/pokemon/images/6/6e/%21.png/revision'
	'/latest/fixed-aspect-ratio-down/width/240/height/240?cb=20130525215832'
	'&fill=transparent'
)


def add_pokemon(folium_map, lat, lon, image_url, name):
	icon = folium.features.CustomIcon(
		image_url,
		icon_size=(50, 50),
	)
	folium.Marker(
		[lat, lon],
		tooltip=name,
		icon=icon,
	).add_to(folium_map)


def show_all_pokemons(request):
	folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)

	pokemons_on_page = []
	time_now = localtime()

	pokemon_entities = PokemonEntity.objects.filter(appeared_at__lt=time_now,
	                                                disappeared_at__gt=time_now)
	for pokemon_entity in pokemon_entities:
		latitude = pokemon_entity.lat
		longitude = pokemon_entity.lon
		image_url = request.build_absolute_uri(pokemon_entity.pokemon.picture.url)

		add_pokemon(folium_map, latitude, longitude, image_url, pokemon_entity.pokemon.title)

	ids_pokemons_on_page = pokemon_entities.values_list('pokemon__id', flat=True).distinct()
	pokemons = Pokemon.objects.filter(id__in=ids_pokemons_on_page)

	for pokemon in pokemons:
		pokemons_on_page.append({
			'pokemon_id': pokemon.id,
			'img_url': request.build_absolute_uri(pokemon.picture.url),
			'title_ru': pokemon.title,
		})

	return render(request, 'mainpage.html', context={
		'map': folium_map._repr_html_(),
		'pokemons': pokemons_on_page,
	})


def generate_pokemon_info(pokemon, request):
	pokemon_info = {"pokemon_id": pokemon.id,
	                "title_ru": pokemon.title,
	                "title_en": pokemon.title_en,
	                "title_jp": pokemon.title_jp,
	                "description": pokemon.description,
	                "img_url": request.build_absolute_uri(pokemon.picture.url),
	                }

	next_evolution = pokemon.next_evolutions.first()

	if next_evolution:
		pokemon_info['next_evolution'] = {
			"title_ru": next_evolution.title,
			"pokemon_id": next_evolution.id,
			"img_url": request.build_absolute_uri(next_evolution.picture.url)
		}

	if pokemon.previous_evolution:
		pokemon_info['previous_evolution'] = {
			"title_ru": pokemon.previous_evolution.title,
			"pokemon_id": pokemon.previous_evolution.id,
			"img_url": request.build_absolute_uri(pokemon.previous_evolution.picture.url)
		}

	return pokemon_info


def show_pokemon(request, pokemon_id):
	pokemon = get_object_or_404(Pokemon, id=pokemon_id)
	time_now = localtime()
	pokemon_entities = PokemonEntity.objects.filter(pokemon=pokemon_id,
	                                                appeared_at__lt=time_now,
	                                                disappeared_at__gt=time_now)

	folium_map = folium.Map(location=MOSCOW_CENTER, zoom_start=12)
	for pokemon_entity in pokemon_entities:
		latitude = pokemon_entity.lat
		longitude = pokemon_entity.lon
		image_url = request.build_absolute_uri(pokemon_entity.pokemon.picture.url)

		add_pokemon(folium_map, latitude, longitude, image_url, pokemon_entity.pokemon.title)

	pokemon = generate_pokemon_info(pokemon, request)

	return render(request, 'pokemon.html', context={
		'map': folium_map._repr_html_(), 'pokemon': pokemon
	})
