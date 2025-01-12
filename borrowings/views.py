from rest_framework import generics

from borrowings.models import Borrowing
from borrowings.serializers import BorrowingSerializer


class BorrowingListView(generics.ListAPIView):
    serializer_class = BorrowingSerializer

    def get_queryset(self):
        user_id = self.request.query_params.get("user_id", None)
        is_active = self.request.query_params.get("is_active", "true") == "true"
        if is_active:
            return Borrowing.objects.filter(user_id=user_id, actual_return_date__isnull=True)
        else:
            return Borrowing.objects.filter(user_id=user_id)


class BorrowingDetailView(generics.RetrieveAPIView):
    queryset = Borrowing.objects.select_related("book", "user")
    serializer_class = BorrowingSerializer
