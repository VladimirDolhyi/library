from rest_framework import generics, permissions, status
from rest_framework.response import Response

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    CreateBorrowingSerializer,
    ReturnBorrowingSerializer
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


class ReturnBorrowingView(generics.CreateAPIView):
    serializer_class = ReturnBorrowingSerializer
    queryset = Borrowing.objects.select_related("book", "user")

    def post(self, request, pk):
        try:
            borrowing = Borrowing.objects.get(pk=pk)
        except Borrowing.DoesNotExist:
            return Response(
                {
                    "detail": "Borrowing not found."
                },
                status=status.HTTP_404_NOT_FOUND
            )

        if borrowing.is_returned:
            return Response(
                {"detail": "This borrowing has already been returned."},
                status=status.HTTP_400_BAD_REQUEST,
            )

        # Set actual return date
        borrowing.actual_return_date = request.data.get(
            "actual_return_date"
        )  # You may send the date via payload or use today
        borrowing.save()

        # Update book inventory
        book = borrowing.book
        book.inventory += 1
        book.save()

        return Response(
            BorrowingSerializer(borrowing).data, status=status.HTTP_200_OK
        )
