from rest_framework import viewsets

from payments.models import Payment
from payments.serializers import PaymentSerializer


class PaymentViewSet(viewsets.ModelViewSet):
    serializer_class = PaymentSerializer
    queryset = Payment.objects.select_related("borrowing")

    def get_queryset(self):
        queryset = self.queryset
        if self.request.user.is_staff:
            return queryset
        return queryset.filter(user=self.request.user)
