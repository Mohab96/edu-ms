from django.db import models
from uuid import uuid4
from django.conf import settings


class User(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    rating = models.DecimalField(max_digits=3, decimal_places=1)
    bio = models.TextField(null=True, blank=True)

    def __str__(self):
        return f'{self.user.username}'


class Course(models.Model):
    name = models.CharField(max_length=250)
    description = models.TextField()
    created_by = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='courses')
    last_update = models.DateField(auto_now=True)
    requirements = models.TextField(null=True, blank=True)
    objectives = models.TextField(null=True, blank=True)
    price = models.IntegerField()
    category = models.ForeignKey('Category', on_delete=models.SET_NULL,
                                 related_name='courses', null=True, blank=True)
    welcome_message = models.CharField(max_length=250)

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
    student = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='cart')
    total_price = models.IntegerField()


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)


class CourseContent(models.Model):
    course = models.OneToOneField(
        Course, on_delete=models.CASCADE, related_name='content')


class Section(models.Model):
    course_content = models.ForeignKey(
        CourseContent, on_delete=models.CASCADE, related_name='sections')


class MaterialItem(models.Model):
    section = models.ForeignKey(
        Section, on_delete=models.CASCADE, related_name='items')
    name = models.CharField(max_length=250)

    # file TODO


class Question(models.Model):
    user = models.ForeignKey(User, on_delete=models.SET_NULL,
                             related_name='questions', null=True, blank=True)

    body = models.CharField(max_length=250)
    answered = models.BooleanField(default=False)


class Answer(models.Model):
    question = models.OneToOneField(
        Question, on_delete=models.CASCADE, related_name='answer')
    body = models.CharField(max_length=250)


class Enrollment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
