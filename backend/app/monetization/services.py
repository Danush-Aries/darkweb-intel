import stripe
import paypalrestsdk
import razorpay
from typing import Optional, Dict, Any
from tortoise.transactions import in_transaction
from ..core.config import settings
from .models import Product, Order, Subscription, Affiliate, Referral, UpsellOffer, PaymentTransaction, OrderStatus, SubscriptionStatus


class PaymentService:
    """Handle payment processing for Stripe, PayPal, and Razorpay"""
    
    def __init__(self):
        # Initialize Stripe
        stripe.api_key = settings.STRIPE_SECRET_KEY
        
        # Initialize PayPal
        paypalrestsdk.configure({
            "mode": "sandbox",  # or "live"
            "client_id": settings.PAYPAL_CLIENT_ID,
            "client_secret": settings.PAYPAL_CLIENT_SECRET
        })
        
        # Initialize Razorpay
        self.razorpay_client = razorpay.Client(
            auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
        )
    
    async def create_stripe_payment_intent(self, amount: float, currency: str = "usd", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a Stripe payment intent"""
        try:
            intent = stripe.PaymentIntent.create(
                amount=int(amount * 100),  # Convert to cents
                currency=currency.lower(),
                metadata=metadata or {}
            )
            return {
                "success": True,
                "client_secret": intent.client_secret,
                "payment_intent_id": intent.id
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_paypal_order(self, amount: float, currency: str = "USD", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a PayPal order"""
        try:
            payment = paypalrestsdk.Payment({
                "intent": "sale",
                "payer": {
                    "payment_method": "paypal"
                },
                "redirect_urls": {
                    "return_url": "http://localhost:3000/payment/success",
                    "cancel_url": "http://localhost:3000/payment/cancel"
                },
                "transactions": [{
                    "item_list": {
                        "items": [{
                            "name": "Product Purchase",
                            "sku": "product",
                            "price": str(amount),
                            "currency": currency,
                            "quantity": 1
                        }]
                    },
                    "amount": {
                        "total": str(amount),
                        "currency": currency
                    },
                    "description": "Product purchase"
                }]
            })
            
            if payment.create():
                return {
                    "success": True,
                    "payment_id": payment.id,
                    "approval_url": next(link.href for link in payment.links if link.rel == "approval_url")
                }
            else:
                return {
                    "success": False,
                    "error": payment.error
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def create_razorpay_order(self, amount: float, currency: str = "INR", metadata: Dict[str, Any] = None) -> Dict[str, Any]:
        """Create a Razorpay order"""
        try:
            order_data = {
                "amount": int(amount * 100),  # Convert to paise
                "currency": currency.upper(),
                "receipt": f"receipt_{metadata.get('timestamp', 'unknown')}" if metadata else "receipt_unknown",
                "payment_capture": 1  # Auto capture
            }
            
            order = self.razorpay_client.order.create(data=order_data)
            
            return {
                "success": True,
                "order_id": order["id"],
                "amount": order["amount"],
                "currency": order["currency"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def verify_stripe_payment(self, payment_intent_id: str) -> Dict[str, Any]:
        """Verify a Stripe payment"""
        try:
            intent = stripe.PaymentIntent.retrieve(payment_intent_id)
            return {
                "success": True,
                "status": intent.status,
                "amount": intent.amount / 100,  # Convert from cents
                "currency": intent.currency
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def verify_paypal_payment(self, payment_id: str, payer_id: str) -> Dict[str, Any]:
        """Verify a PayPal payment"""
        try:
            payment = paypalrestsdk.Payment.find(payment_id)
            
            if payment.execute({"payer_id": payer_id}):
                return {
                    "success": True,
                    "status": payment.state,
                    "amount": payment.transactions[0].amount.total,
                    "currency": payment.transactions[0].amount.currency
                }
            else:
                return {
                    "success": False,
                    "error": payment.error
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def verify_razorpay_payment(self, order_id: str, payment_id: str, signature: str) -> Dict[str, Any]:
        """Verify a Razorpay payment"""
        try:
            # Verify signature
            params_dict = {
                'razorpay_order_id': order_id,
                'razorpay_payment_id': payment_id,
                'razorpay_signature': signature
            }
            
            self.razorpay_client.utility.verify_payment_signature(params_dict)
            
            # Fetch payment details
            payment = self.razorpay_client.payment.fetch(payment_id)
            
            return {
                "success": True,
                "status": payment["status"],
                "amount": payment["amount"] / 100,  # Convert from paise
                "currency": payment["currency"]
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class SubscriptionService:
    """Handle subscription management"""
    
    def __init__(self, payment_service: PaymentService):
        self.payment_service = payment_service
    
    async def create_stripe_subscription(self, product: Product, customer_email: str, customer_name: str = None, trial_days: int = 0) -> Dict[str, Any]:
        """Create a Stripe subscription"""
        try:
            # Create or get customer
            customers = stripe.Customer.list(email=customer_email, limit=1)
            if customers.data:
                customer = customers.data[0]
            else:
                customer = stripe.Customer.create(
                    email=customer_email,
                    name=customer_name or customer_email.split('@')[0]
                )
            
            # Create subscription
            subscription = stripe.Subscription.create(
                customer=customer.id,
                items=[{
                    "price_data": {
                        "currency": product.currency.lower(),
                        "product_data": {
                            "name": product.name,
                            "description": product.description
                        },
                        "unit_amount": int(product.price * 100),
                        "recurring": {
                            "interval": product.billing_interval or "month"
                        }
                    }
                }],
                trial_period_days=trial_days if trial_days > 0 else None,
                metadata={
                    "product_id": str(product.id),
                    "customer_email": customer_email
                }
            )
            
            return {
                "success": True,
                "subscription_id": subscription.id,
                "client_secret": subscription.latest_invoice.payment_intent.client_secret if subscription.latest_invoice else None,
                "status": subscription.status
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def cancel_subscription(self, subscription_id: str, gateway: str = "stripe") -> Dict[str, Any]:
        """Cancel a subscription"""
        try:
            if gateway.lower() == "stripe":
                subscription = stripe.Subscription.modify(
                    subscription_id,
                    cancel_at_period_end=True
                )
                return {
                    "success": True,
                    "status": subscription.status,
                    "cancel_at_period_end": subscription.cancel_at_period_end
                }
            # Add PayPal and Razorpay cancellation logic here
            else:
                return {
                    "success": False,
                    "error": f"Gateway {gateway} not supported for cancellation yet"
                }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


class AffiliateService:
    """Handle affiliate and referral management"""
    
    async def create_affiliate(self, name: str, email: str, commission_rate: float = 10.0) -> Dict[str, Any]:
        """Create a new affiliate"""
        try:
            # Check if affiliate already exists
            existing = await Affiliate.get_or_none(email=email)
            if existing:
                return {
                    "success": False,
                    "error": "Affiliate with this email already exists"
                }
            
            affiliate = await Affiliate.create(
                name=name,
                email=email,
                commission_rate=commission_rate
            )
            
            return {
                "success": True,
                "affiliate": {
                    "id": affiliate.id,
                    "name": affiliate.name,
                    "email": affiliate.email,
                    "commission_rate": float(affiliate.commission_rate)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }
    
    async def track_referral(self, affiliate_id: int, referred_email: str, order_id: int = None, subscription_id: int = None) -> Dict[str, Any]:
        """Track a referral and calculate commission"""
        try:
            affiliate = await Affiliate.get(id=affiliate_id)
            if not affiliate:
                return {
                    "success": False,
                    "error": "Affiliate not found"
                }
            
            # Calculate commission amount
            commission_amount = 0.0
            if order_id:
                order = await Order.get(id=order_id)
                if order:
                    commission_amount = float(order.amount) * (float(affiliate.commission_rate) / 100)
            elif subscription_id:
                subscription = await Subscription.get(id=subscription_id)
                if subscription:
                    # For subscriptions, commission might be recurring or one-time
                    commission_amount = float(subscription.amount) * (float(affiliate.commission_rate) / 100)
            
            referral = await Referral.create(
                affiliate=affiliate,
                referred_email=referred_email,
                order_id=order_id,
                subscription_id=subscription_id,
                commission_earned=commission_amount
            )
            
            return {
                "success": True,
                "referral": {
                    "id": referral.id,
                    "commission_earned": float(referral.commission_earned)
                }
            }
        except Exception as e:
            return {
                "success": False,
                "error": str(e)
            }


# Service instances
payment_service = PaymentService()
subscription_service = SubscriptionService(payment_service)
affiliate_service = AffiliateService()