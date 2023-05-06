from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()


class Tag(models.Model):
    name = models.CharField(verbose_name='Имя тэга',
                            max_length=200, unique=True)
    color = models.CharField(verbose_name='Цвет тэга',
                             max_length=7, unique=True)
    slug = models.SlugField(verbose_name='Слаг', max_length=200,
                            unique=True)

    def __str__(self):
        return f'{self.name} цвет {self.color}'

    class Meta:
        verbose_name = 'Тэг'
        verbose_name_plural = 'Тэги'
        ordering = ('name', )


class Ingredient(models.Model):
    name = models.CharField(verbose_name='Имя ингредиента', max_length=150)
    measurement_unit = models.CharField(
        verbose_name='Единицы измерения', max_length=10)

    def __str__(self):
        return f'{self.name} {self.measurement_unit}'

    class Meta:
        verbose_name = 'Ингредиент'
        verbose_name_plural = 'Ингредиенты'


class Recipe(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               verbose_name='Автор рецепта',
                               related_name='recipes')
    name = models.CharField(max_length=200, verbose_name='Название рецепта')
    text = models.TextField(verbose_name='Текст рецепта')
    cooking_time = models.PositiveSmallIntegerField()
    image = models.ImageField(
        verbose_name='Фото блюда', upload_to='recipe_images/',
        default=None, null=True)
    tags = models.ManyToManyField(
        Tag, through='TagRecipe')
    ingredients = models.ManyToManyField(
        Ingredient, through='IngredientRecipe', through_fields=('recipe',
                                                                'ingredient'))
    pub_date = models.DateTimeField(
        verbose_name='Дата публикации',
        auto_now_add=True,
        editable=False,
    )

    def __str__(self) -> str:
        return f'{self.name}. Автор: {self.author}'

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'
        ordering = ('-pub_date',)


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингридиентов')

    def __str__(self):
        return f'{self.ingredient} {self.recipe}'

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            verbose_name='Тэги рецепта')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')

    def __str__(self):
        return f'{self.tag} {self.recipe}'

    class Meta:
        verbose_name = 'Ингредиент рецепта'
        verbose_name_plural = 'Ингредиенты рецепта'


class FavoriteRecipe(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='favorite',
        verbose_name='Пользователь'
    )
    favorite_recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='favorite_recipe',
        verbose_name='Избранный рецепт'
    )

    class Meta:
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'favorite_recipe'),
                name='unique favourite')]
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = ('id',)

    def __str__(self):
        return (f'Пользователь: {self.user.username}'
                f'рецепт: {self.favorite_recipe.name}')


class ShoppingCart(models.Model):
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='shopping_cart',
        verbose_name='Пользователь'
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name='recipe_shopping_cart',
        verbose_name='Рецепт'
    )

    class Meta:
        ordering = ('id',)
        constraints = [
            models.UniqueConstraint(
                fields=('user', 'recipe'),
                name='unique recipe in shopping cart')]
        verbose_name = 'Список покупок'
        verbose_name_plural = 'Список покупок'

    def __str__(self):
        return (f'Пользователь: {self.user.username},'
                f'рецепт в списке: {self.recipe.name}')
