from django.db import models
from django.urls import reverse, NoReverseMatch

class Menu(models.Model):
    name = models.CharField(max_length=100, unique=True, default='')

    class Meta:
        verbose_name = "Меню"
        verbose_name_plural = "Меню"

    def __str__(self):
        return self.name


class MenuItem(models.Model):
    menu = models.ForeignKey(Menu, related_name='items', on_delete=models.CASCADE, default='')
    title = models.CharField(max_length=100)
    url = models.CharField(
        max_length=255,
        blank=True,
        help_text="Явный URL. Игнорируется, если указан named_url."
    )
    named_url = models.CharField(
        max_length=100,
        blank=True,
        help_text="Имя маршрута (например, 'contact'). Приоритетное поле!!!"
    )
    parent = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        related_name='children',
        on_delete=models.CASCADE
    )

    def get_absolute_url(self):
        if self.named_url:
            try:
                return reverse(self.named_url)
            except NoReverseMatch:
                return '#'
        return self.url or '#'

    class Meta:
        verbose_name = "Пункты меню"
        verbose_name_plural = "Пункты меню"

    def __str__(self):
        return self.title



