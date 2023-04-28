from django.db import models

from users.models import User


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

    class Meta:
        verbose_name = 'Рецепт'
        verbose_name_plural = 'Рецепты'

    def __str__(self) -> str:
        return f'{self.name}. Автор: {self.author}'


class IngredientRecipe(models.Model):
    ingredient = models.ForeignKey(
        Ingredient, on_delete=models.CASCADE, verbose_name='Ингредиент')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')
    amount = models.PositiveIntegerField(
        verbose_name='Количество ингридиентов')


class TagRecipe(models.Model):
    tag = models.ForeignKey(Tag, on_delete=models.CASCADE,
                            verbose_name='Тэги рецепта')
    recipe = models.ForeignKey(
        Recipe, on_delete=models.CASCADE, verbose_name='Рецепт')


class Favorite(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    class Meta:
        verbose_name = 'Избранное'
        verbose_name_plural = 'Избранные'
        ordering = ['-id']
        constraints = [
            models.UniqueConstraint(
                fields=['user', 'recipe'],
                name='unique_favorite_user_recipe'
            )
        ]


class Carts(models.Model):

    recipe = models.ForeignKey(
        verbose_name='Рецепты в списке покупок',
        related_name='in_carts',
        to=Recipe,
        on_delete=models.CASCADE,
    )
    user = models.ForeignKey(
        verbose_name='Владелец списка',
        related_name='carts',
        to=User,
        on_delete=models.CASCADE,
    )
    date_added = models.DateTimeField(
        verbose_name='Дата добавления',
        auto_now_add=True,
        editable=False
    )

    class Meta:
        verbose_name = 'Рецепт в корзине'
        verbose_name_plural = 'Рецепты в корзине'
        constraints = (
            models.UniqueConstraint(
                fields=('recipe', 'user', ),
                name='\n%(app_label)s_%(class)s рецепт уже в корзине\n',
            ),
        )
