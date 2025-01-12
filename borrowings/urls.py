from django.urls import path

from borrowings.views import (
    BorrowingListCreateView, BorrowingDetail,
)

app_name = "borrowings"

urlpatterns = [
    path(
        "borrowings/",
        BorrowingListCreateView.as_view(),
        name="borrowings-list-create"
    ),
    path(
        "borrowings/<int:pk>/",
        BorrowingDetail.as_view(),
        name="borrowing-detail"
    )
]
