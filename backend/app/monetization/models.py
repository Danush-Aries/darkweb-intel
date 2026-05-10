from tortoise import fields, models
from enum import IntEnum


class ProductType(IntEnum):
    COURSE = 1
    EBOOK = 2
    SAAS = 3
    MEMBERSHIP = 4


class Product(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    product_type = fields.IntField(choices=[(e.value, e.name) for e in ProductType])
    price = fields.DecimalField(max_digits=10, decimal_places=2)
    currency = fields.CharField(max_length=3, default="USD")
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    # For SaaS: billing interval (monthly, yearly)
    billing_interval = fields.CharField(max_length=20, null=True)  # e.g., 'month', 'year'
    # For courses/ebooks: download URL or access code
    access_info = fields.TextField(null=True)

    class Meta:
        table = "products"


class OrderStatus(IntEnum):
    PENDING = 1
    PAID = 2
    FAILED = 3
    REFUNDED = 4


class Order(models.Model):
    id = fields.IntField(pk=True)
    product = fields.ForeignKeyField('models.Product', related_name='orders')
    customer_email = fields.CharField(max_length=255)
    customer_name = fields.CharField(max_length=255, null=True)
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    currency = fields.CharField(max_length=3, default="USD")
    status = fields.IntField(choices=[(e.value, e.name) for e in OrderStatus], default=OrderStatus.PENDING)
    stripe_payment_intent_id = fields.CharField(max_length=255, null=True, unique=True)
    paypal_order_id = fields.CharField(max_length=255, null=True, unique=True)
    razorpay_order_id = fields.CharField(max_length=255, null=True, unique=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "orders"


class SubscriptionStatus(IntEnum):
    ACTIVE = 1
    CANCELED = 2
    PAST_DUE = 3
    UNPAID = 4
    TRIALING = 5


class Subscription(models.Model):
    id = fields.IntField(pk=True)
    product = fields.ForeignKeyField('models.Product', related_name='subscriptions')
    customer_email = fields.CharField(max_length=255)
    customer_name = fields.CharField(max_length=255, null=True)
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    currency = fields.CharField(max_length=3, default="USD")
    status = fields.IntField(choices=[(e.value, e.name) for e in SubscriptionStatus], default=SubscriptionStatus.ACTIVE)
    stripe_subscription_id = fields.CharField(max_length=255, null=True, unique=True)
    paypal_subscription_id = fields.CharField(max_length=255, null=True, unique=True)
    razorpay_subscription_id = fields.CharField(max_length=255, null=True, unique=True)
    current_period_start = fields.DatetimeField(null=True)
    current_period_end = fields.DatetimeField(null=True)
    cancel_at_period_end = fields.BooleanField(default=False)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "subscriptions"


class Affiliate(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    email = fields.CharField(max_length=255, unique=True)
    commission_rate = fields.DecimalField(max_digits=5, decimal_places=2)  # percentage
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "affiliates"


class Referral(models.Model):
    id = fields.IntField(pk=True)
    affiliate = fields.ForeignKeyField('models.Affiliate', related_name='referrals')
    referred_email = fields.CharField(max_length=255)
    order = fields.ForeignKeyField('models.Order', related_name='referrals', null=True)
    subscription = fields.ForeignKeyField('models.Subscription', related_name='referrals', null=True)
    commission_earned = fields.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "referrals"


class UpsellOffer(models.Model):
    id = fields.IntField(pk=True)
    name = fields.CharField(max_length=255)
    description = fields.TextField()
    product = fields.ForeignKeyField('models.Product', related_name='upsell_offers')
    trigger_product = fields.ForeignKeyField('models.Product', related_name='triggered_upsells')
    discount_percentage = fields.DecimalField(max_digits=5, decimal_places=2, default=0.00)
    is_active = fields.BooleanField(default=True)
    created_at = fields.DatetimeField(auto_now_add=True)
    updated_at = fields.DatetimeField(auto_now=True)

    class Meta:
        table = "upsell_offers"


class PaymentTransaction(models.Model):
    id = fields.IntField(pk=True)
    order = fields.ForeignKeyField('models.Order', related_name='transactions', null=True)
    subscription = fields.ForeignKeyField('models.Subscription', related_name='transactions', null=True)
    amount = fields.DecimalField(max_digits=10, decimal_places=2)
    currency = fields.CharField(max_length=3, default="USD")
    gateway = fields.CharField(max_length=50)  # 'stripe', 'paypal', 'razorpay'
    gateway_transaction_id = fields.CharField(max_length=255, unique=True)
    status = fields.CharField(max_length=50)  # e.g., 'succeeded', 'failed', 'pending'
    created_at = fields.DatetimeField(auto_now_add=True)

    class Meta:
        table = "payment_transactions"