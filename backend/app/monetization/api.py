from fastapi import APIRouter, HTTPException, Depends, BackgroundTasks
from typing import List, Optional
from app.monetization.models import (
    Product, Order, Subscription, Affiliate, Referral, UpsellOffer,
    ProductType, OrderStatus, SubscriptionStatus
)
from app.monetization.services import (
    payment_service, subscription_service, affiliate_service
)
from pydantic import BaseModel, EmailField
from tortoise.exceptions import DoesNotExist

router = APIRouter()


# Pydantic models for request/response
class ProductBase(BaseModel):
    name: str
    description: str
    product_type: int  # ProductType enum value
    price: float
    currency: str = "USD"
    billing_interval: Optional[str] = None
    access_info: Optional[str] = None

class ProductCreate(ProductBase):
    pass

class ProductResponse(ProductBase):
    id: int
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class OrderBase(BaseModel):
    product_id: int
    customer_email: EmailField
    customer_name: Optional[str] = None

class OrderCreate(OrderBase):
    payment_gateway: str  # stripe, paypal, razorpay

class OrderResponse(OrderBase):
    id: int
    amount: float
    currency: str
    status: int
    stripe_payment_intent_id: Optional[str] = None
    paypal_order_id: Optional[str] = None
    razorpay_order_id: Optional[str] = None
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class SubscriptionBase(BaseModel):
    product_id: int
    customer_email: EmailField
    customer_name: Optional[str] = None
    trial_days: int = 0

class SubscriptionCreate(SubscriptionBase):
    payment_gateway: str  # stripe, paypal, razorpay

class SubscriptionResponse(SubscriptionBase):
    id: int
    amount: float
    currency: str
    status: int
    stripe_subscription_id: Optional[str] = None
    paypal_subscription_id: Optional[str] = None
    razorpay_subscription_id: Optional[str] = None
    current_period_start: Optional[str] = None
    current_period_end: Optional[str] = None
    cancel_at_period_end: bool
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class AffiliateBase(BaseModel):
    name: str
    email: EmailField
    commission_rate: float = 10.0

class AffiliateCreate(AffiliateBase):
    pass

class AffiliateResponse(AffiliateBase):
    id: int
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


class ReferralBase(BaseModel):
    affiliate_id: int
    referred_email: EmailField
    order_id: Optional[int] = None
    subscription_id: Optional[int] = None

class ReferralCreate(ReferralBase):
    pass

class ReferralResponse(ReferralBase):
    id: int
    commission_earned: float
    created_at: str

    class Config:
        orm_mode = True


class UpsellOfferBase(BaseModel):
    name: str
    description: str
    product_id: int
    trigger_product_id: int
    discount_percentage: float = 0.0

class UpsellOfferCreate(UpsellOfferBase):
    pass

class UpsellOfferResponse(UpsellOfferBase):
    id: int
    is_active: bool
    created_at: str
    updated_at: str

    class Config:
        orm_mode = True


# Product endpoints
@router.post("/products/", response_model=ProductResponse)
async def create_product(product: ProductCreate):
    """Create a new product"""
    db_product = await Product.create(**product.dict())
    return db_product

@router.get("/products/", response_model=List[ProductResponse])
async def list_products(active_only: bool = True):
    """List all products"""
    if active_only:
        products = await Product.filter(is_active=True)
    else:
        products = await Product.all()
    return products

@router.get("/products/{product_id}", response_model=ProductResponse)
async def get_product(product_id: int):
    """Get a specific product"""
    try:
        product = await Product.get(id=product_id)
        return product
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")


# Order endpoints
@router.post("/orders/", response_model=OrderResponse)
async def create_order(order: OrderCreate, background_tasks: BackgroundTasks):
    """Create a new order and initiate payment"""
    try:
        product = await Product.get(id=order.product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Create order record
    db_order = await Order.create(
        product=product,
        customer_email=order.customer_email,
        customer_name=order.customer_name,
        amount=product.price,
        currency=product.currency
    )
    
    # Process payment based on gateway
    payment_result = None
    if order.payment_gateway.lower() == "stripe":
        payment_result = await payment_service.create_stripe_payment_intent(
            amount=product.price,
            currency=product.currency.lower(),
            metadata={"order_id": db_order.id, "product_id": product.id}
        )
        if payment_result["success"]:
            db_order.stripe_payment_intent_id = payment_result["payment_intent_id"]
    elif order.payment_gateway.lower() == "paypal":
        payment_result = await payment_service.create_paypal_order(
            amount=product.price,
            currency=product.currency,
            metadata={"order_id": db_order.id, "product_id": product.id}
        )
        if payment_result["success"]:
            db_order.paypal_order_id = payment_result["payment_id"]
    elif order.payment_gateway.lower() == "razorpay":
        payment_result = await payment_service.create_razorpay_order(
            amount=product.price,
            currency=product.currency,
            metadata={"order_id": db_order.id, "product_id": product.id}
        )
        if payment_result["success"]:
            db_order.razorpay_order_id = payment_result["order_id"]
    else:
        raise HTTPException(status_code=400, detail="Unsupported payment gateway")
    
    await db_order.save()
    
    if not payment_result or not payment_result["success"]:
        db_order.status = OrderStatus.FAILED
        await db_order.save()
        raise HTTPException(status_code=400, detail=payment_result.get("error", "Payment initiation failed"))
    
    # Update order status to pending payment
    db_order.status = OrderStatus.PENDING
    await db_order.save()
    
    # Return order with payment details
    response_data = await Order.get(id=db_order.id)
    if order.payment_gateway.lower() == "stripe":
        response_data.stripe_payment_intent_id = payment_result["payment_intent_id"]
    elif order.payment_gateway.lower() == "paypal":
        response_data.paypal_order_id = payment_result["payment_id"]
    elif order.payment_gateway.lower() == "razorpay":
        response_data.razorpay_order_id = payment_result["order_id"]
    
    return response_data


# Subscription endpoints
@router.post("/subscriptions/", response_model=SubscriptionResponse)
async def create_subscription(subscription: SubscriptionCreate, background_tasks: BackgroundTasks):
    """Create a new subscription and initiate payment"""
    try:
        product = await Product.get(id=subscription.product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # For subscription products, verify it's a SaaS or membership type
    if product.product_type not in [ProductType.SAAS.value, ProductType.MEMBERSHIP.value]:
        raise HTTPException(status_code=400, detail="Product is not a subscription type")
    
    # Create subscription record
    db_subscription = await Subscription.create(
        product=product,
        customer_email=subscription.customer_email,
        customer_name=subscription.customer_name,
        amount=product.price,
        currency=product.currency
    )
    
    # Process payment based on gateway
    payment_result = None
    if subscription.payment_gateway.lower() == "stripe":
        payment_result = await subscription_service.create_stripe_subscription(
            product=product,
            customer_email=subscription.customer_email,
            customer_name=subscription.customer_name,
            trial_days=subscription.trial_days
        )
        if payment_result["success"]:
            db_subscription.stripe_subscription_id = payment_result["subscription_id"]
    # Add PayPal and Razorpay subscription logic here
    else:
        raise HTTPException(status_code=400, detail="Subscription gateway not supported yet")
    
    await db_subscription.save()
    
    if not payment_result or not payment_result["success"]:
        db_subscription.status = SubscriptionStatus.PAST_DUE
        await db_subscription.save()
        raise HTTPException(status_code=400, detail=payment_result.get("error", "Subscription initiation failed"))
    
    # Update subscription status
    db_subscription.status = SubscriptionStatus.ACTIVE if subscription.trial_days == 0 else SubscriptionStatus.TRIALING
    if payment_result.get("current_period_start"):
        db_subscription.current_period_start = payment_result["current_period_start"]
    if payment_result.get("current_period_end"):
        db_subscription.current_period_end = payment_result["current_period_end"]
    
    await db_subscription.save()
    
    # Return subscription with payment details
    response_data = await Subscription.get(id=db_subscription.id)
    if subscription.payment_gateway.lower() == "stripe":
        response_data.stripe_subscription_id = payment_result["subscription_id"]
    # Add other gateways
    
    return response_data


# Affiliate endpoints
@router.post("/affiliates/", response_model=AffiliateResponse)
async def create_affiliate(affiliate: AffiliateCreate):
    """Create a new affiliate"""
    result = await affiliate_service.create_affiliate(
        name=affiliate.name,
        email=affiliate.email,
        commission_rate=affiliate.commission_rate
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result["affiliate"]


@router.post("/referrals/", response_model=ReferralResponse)
async def track_referral(referral: ReferralCreate):
    """Track a referral"""
    # Verify affiliate exists
    try:
        affiliate = await Affiliate.get(id=referral.affiliate_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Affiliate not found")
    
    # Verify order or subscription if provided
    if referral.order_id:
        try:
            await Order.get(id=referral.order_id)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Order not found")
    
    if referral.subscription_id:
        try:
            await Subscription.get(id=referral.subscription_id)
        except DoesNotExist:
            raise HTTPException(status_code=404, detail="Subscription not found")
    
    result = await affiliate_service.track_referral(
        affiliate_id=referral.affiliate_id,
        referred_email=referral.referred_email,
        order_id=referral.order_id,
        subscription_id=referral.subscription_id
    )
    
    if not result["success"]:
        raise HTTPException(status_code=400, detail=result["error"])
    
    return result["referral"]


# Upsell endpoints
@router.post("/upsell-offers/", response_model=UpsellOfferResponse)
async def create_upsell_offer(upsell: UpsellOfferCreate):
    """Create a new upsell offer"""
    # Verify products exist
    try:
        product = await Product.get(id=upsell.product_id)
        trigger_product = await Product.get(id=upsell.trigger_product_id)
    except DoesNotExist:
        raise HTTPException(status_code=404, detail="Product not found")
    
    db_upsell = await UpsellOffer.create(**upsell.dict())
    return db_upsell


# Webhook endpoints for payment gateways
@router.post("/webhooks/stripe")
async def stripe_webhook(request: dict):
    """Handle Stripe webhooks"""
    # Implementation would verify signature and handle events
    # For now, just acknowledge receipt
    return {"status": "received"}

@router.post("/webhooks/paypal")
async def paypal_webhook(request: dict):
    """Handle PayPal webhooks"""
    return {"status": "received"}

@router.post("/webhooks/razorpay")
async def razorpay_webhook(request: dict):
    """Handle Razorpay webhooks"""
    return {"status": "received"}