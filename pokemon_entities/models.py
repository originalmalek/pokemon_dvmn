from django.db import models


class Pokemon(models.Model):
	title = models.CharField(max_length=200)
	title_en = models.CharField(max_length=200, blank=True)
	title_jp = models.CharField(max_length=200, blank=True)
	picture = models.ImageField(upload_to='pokemon_pics', null=True)
	description = models.TextField(blank=True)

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

	lat = models.FloatField()
	lon = models.FloatField()

	appeared_at = models.DateTimeField(null=True)
	disappeared_at = models.DateTimeField(null=True, blank=True)

	level = models.IntegerField(default=0)
	health = models.IntegerField(default=0)
	strength = models.IntegerField(default=0)
	defence = models.IntegerField(default=0)
	stamina = models.IntegerField(default=0)
