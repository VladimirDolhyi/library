from rest_framework.permissions import SAFE_METHODS, BasePermission


class IsAdminOrReadOnly(BasePermission):
    """
    Custom permission to only allow admin users to edit or delete books.
    All users can view (GET) the books.
    """

    def has_permission(self, request, view):
        # Allow any user to view (GET) books.
        if request.method in SAFE_METHODS:
            return True
        # Allow only admin users to create/update/delete books.
        return request.user and request.user.is_staff
