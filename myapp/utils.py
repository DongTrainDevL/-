from django.db.models import Sum
from .models import OrderItem

# utils.py


def calculate_total_revenue():
    # ค้นหารายการสั่งซื้อทั้งหมด
    all_orders = OrderItem.objects.all()

    # คำนวณรายได้รวมจากการสั่งซื้อทั้งหมด
    total_revenue = all_orders.aggregate(total_revenue=Sum('food__price'))

    return total_revenue['total_revenue'] if total_revenue['total_revenue'] is not None else 0
