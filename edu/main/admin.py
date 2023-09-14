from django.contrib import admin
from .models import *


admin.site.register(User)
admin.site.register(Course)
admin.site.register(Category)
admin.site.register(Review)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(CourseContent)
admin.site.register(MaterialItem)
admin.site.register(Question)
admin.site.register(Answer)
admin.site.register(Enrollment)
