# from rest_framework import permissions
# from rest_framework.permissions import IsAdminUser
# from .models import Course


# class IsAdminOrOwner(permissions.BasePermission):
#     def has_permission(self, request, view):
#         course = Course.objects.filter(id=view.kwargs['pk']).get('created_by')
#         is_owner = bool(course == self.user.id)
#         return bool(IsAdminUser() or is_owner)
#         # TODO
