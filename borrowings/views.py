from rest_framework import generics, permissions

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer, CreateBorrowingSerializer
)


class BorrowingListCreateView(generics.ListCreateAPIView):
    permission_classes = (permissions.IsAuthenticated,)

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book", "user")

        user = self.request.user
        is_active = self.request.query_params.get(
            "is_active", "true"
        ) == "true"
        user_id = self.request.query_params.get("user_id", None)

        if user.is_staff():
            if user_id:
                queryset = queryset.filter(user_id=user_id)
        else:
            queryset = queryset.filter(user=user)

        if is_active:
            return queryset.filter(
                user_id=user_id, actual_return_date__isnull=True
            )
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BorrowingSerializer
        return CreateBorrowingSerializer

    def perform_create(self, serializer):
        # Attach the current user to the borrowing
        serializer.save(user=self.request.user)


class BorrowingDetail(generics.RetrieveAPIView):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingSerializer
