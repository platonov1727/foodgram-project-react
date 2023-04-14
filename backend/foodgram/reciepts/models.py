from django.db import models
from django.contrib.auth import get_user_model


User = get_user_model()


class Tag(models.Model):
    name = models.CharField(verbose_name='Имя тэга',
                            max_length=200, unique=True)
    color = models.CharField(verbose_name='Цвет тэга',
                             max_length=7, unique=True)
    slug = models.SlugField(verbose_name='Слаг', max_length=200,
                            unique=True)

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name', )

    def __str__(self):
        return f'{self.name} цвет {self.color}'


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Имя ингредиента', max_length=150)
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения', max_length=10)

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'

    def __str__(self):
        return self.name
