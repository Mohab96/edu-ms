import os
from django.db import models
from uuid import uuid4
from django.conf import settings
from django.core.validators import FileExtensionValidator
from django.dispatch import receiver


class User(models.Model):
    core_user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1, default=0)
    bio = models.TextField(default='No Bio')

    def __str__(self):
        return f'{self.core_user.username}'


class Course(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField(null=True, blank=True)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE,
                                   related_name='courses',
                                   blank=False, null=False)
    last_update = models.DateField(auto_now=True)
    requirements = models.TextField(null=True, blank=True)
    objectives = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 related_name='courses', null=True, blank=True)
    welcome_message = models.CharField(max_length=250, null=True, blank=True)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=250)

    def __str__(self):
        return self.name


class Review(models.Model):
    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name='reviews')
    student = models.ForeignKey(User, on_delete=models.SET_NULL,
                                related_name='reviews', null=True, blank=True)
    rating = models.DecimalField(max_digits=3, decimal_places=2)
    body = models.TextField()


class Cart(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4)
    student = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='cart')


class CartItem(models.Model):
    cart = models.ForeignKey(
        Cart, on_delete=models.CASCADE, related_name='items')
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class MaterialItem(models.Model):
    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='items', blank=True, null=True)
    name = models.CharField(max_length=250)
    file = models.FileField(upload_to='main',
                            validators=[
                                FileExtensionValidator(['pdf', 'mp4'])],
                            blank=True, null=True)


@receiver(models.signals.post_delete, sender=MaterialItem)
def auto_delete_file_on_delete(sender, instance, **kwargs):
    """
    Deletes file from filesystem
    when corresponding `MaterialItem` object is deleted.
    """
    if instance.file:
        if os.path.isfile(instance.file.path):
            os.remove(instance.file.path)


@receiver(models.signals.pre_save, sender=MaterialItem)
def auto_delete_file_on_change(sender, instance, **kwargs):
    """
    Deletes old file from filesystem
    when corresponding `MaterialItem` object is updated
    with new file.
    """
    if not instance.pk:
        return False

    try:
        old_file = MaterialItem.objects.get(pk=instance.pk).file
    except MaterialItem.DoesNotExist:
        return False

    new_file = instance.file
    if not old_file == new_file:
        if os.path.isfile(old_file.path):
            os.remove(old_file.path)


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='questions', null=False, blank=False)

    course = models.ForeignKey(Course, on_delete=models.CASCADE,
                               related_name='questions', null=False, blank=False)
    body = models.TextField(null=False, blank=False)


class Answer(models.Model):
    question = models.OneToOneField(Question, on_delete=models.CASCADE,
                                    related_name='answer', null=False, blank=False)
    body = models.CharField(max_length=250)


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
