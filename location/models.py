from django.core.validators import RegexValidator
from django.db import models


class Capital(models.Model):
    """Capital City Model Class"""
    alpha = RegexValidator(
        r'^[a-zA-Z]*$', 'Only alpha characters are allowed.')
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        validators=[alpha]
    )

    class Meta:
        verbose_name = "capital"
        verbose_name_plural = "capitals"
        ordering = ['name']

    def save(self, *args, **kwargs):
        """Ensure capitalization of capital names upon save"""
        if self.name is not None:
            self.name = self.name.title()  # Capitalize first letter
        return super(Capital, self).save(*args, **kwargs)

    def __str__(self):
        return self.name


class State(models.Model):
    """State Model Class"""
    alpha = RegexValidator(
        r'^[a-zA-Z]*$', 'Only alpha characters are allowed.')
    name = models.CharField(
        max_length=100,
        blank=False,
        null=False,
        unique=True,
        validators=[alpha]
    )
    abbr = models.CharField(
        'Abbreviation',
        max_length=2,
        blank=False,
        null=False,
        unique=True,
        validators=[alpha]
    )
    capital = models.ForeignKey(Capital, on_delete=models.CASCADE, null=False)

    class Meta:
        verbose_name = "state"
        verbose_name_plural = "states"
        ordering = ['name']

    def save(self, *args, **kwargs):
        """Ensure capitalization of state names and abbreviations upon save"""
        if self.name is not None:
            self.name = self.name.title()  # Capitalize only first letter
        if self.abbr is not None:
            self.abbr = self.abbr.upper()  # Capitalize all letters
        return super(State, self).save(*args, **kwargs)

    def __str__(self):
        return self.name
