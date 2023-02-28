from django.db import models


class Pokemon(models.Model):
	title = models.CharField(max_length=200, verbose_name='Название покемона')
	title_en = models.CharField(max_length=200, blank=True, verbose_name='Название анг.')
	title_jp = models.CharField(max_length=200, blank=True, verbose_name='Название яп.')
	picture = models.ImageField(upload_to='pokemon_pics',
	                            null=True,
	                            verbose_name='Картинка')
	description = models.TextField(blank=True, verbose_name='Описание')

	previous_evolution = models.ForeignKey('self',
	                                       verbose_name='Из кого эволюционирует',
	                                       null=True,
	                                       blank=True,
	                                       related_name='next_evolutions',
	                                       on_delete=models.CASCADE)

	def __str__(self):
		return self.title


class PokemonEntity(models.Model):
	pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

	lat = models.FloatField(verbose_name='Широта')
	lon = models.FloatField(verbose_name='Долгота')

	appeared_at = models.DateTimeField(null=True, verbose_name='Появился в')
	disappeared_at = models.DateTimeField(null=True,
	                                      blank=True,
	                                      verbose_name='Исчез в')

	level = models.IntegerField(default=0, verbose_name='Уровень покемона')
	health = models.IntegerField(default=0, verbose_name='Здоровье покемона')
	strength = models.IntegerField(default=0, verbose_name='Сила покемона')
	defence = models.IntegerField(default=0, verbose_name='Защита покемона')
	stamina = models.IntegerField(default=0, verbose_name='Выносливость покемона')
