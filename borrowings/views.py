from rest_framework import generics

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer, CreateBorrowingSerializer
)


class BorrowingListCreateView(generics.ListCreateAPIView):

    def get_queryset(self):
        queryset = Borrowing.objects.select_related("book", "user")
        if self.request.method == "GET":
            user_id = self.request.query_params.get("user_id", None)
            is_active = self.request.query_params.get(
                "is_active", "true"
            ) == "true"
            if is_active:
                return queryset.filter(
                    user_id=user_id, actual_return_date__isnull=True
                )
            else:
                return queryset.filter(user_id=user_id)
        return queryset

    def get_serializer_class(self):
        if self.request.method == "GET":
            return BorrowingSerializer
        return CreateBorrowingSerializer

    def perform_create(self, serializer):
        # Attach the current user to the borrowing
        if self.request.method == "POST":
            serializer.save(user=self.request.user)


class BorrowingDetail(generics.RetrieveAPIView):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingSerializer
