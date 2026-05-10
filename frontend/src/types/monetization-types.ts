export type ProductType = 1 | 2 | 3 | 4; // 1: Course, 2: Ebook, 3: SaaS, 4: Membership

export interface Product {
  id: number;
  name: string;
  description: string;
  product_type: ProductType;
  price: number;
  currency: string;
  is_active: boolean;
  billing_interval?: string; // for SaaS: month, year
  access_info?: string; // for courses/ebooks
  created_at: string;
  updated_at: string;
}

export interface Order {
  id: number;
  product_id: number;
  customer_email: string;
  customer_name?: string;
  amount: number;
  currency: string;
  status: number; // 1: Pending, 2: Paid, 3: Failed, 4: Refunded
  stripe_payment_intent_id?: string;
  paypal_order_id?: string;
  razorpay_order_id?: string;
  created_at: string;
  updated_at: string;
}

export interface Subscription {
  id: number;
  product_id: number;
  customer_email: string;
  customer_name?: string;
  amount: number;
  currency: string;
  status: number; // 1: Active, 2: Canceled, 3: Past Due, 4: Unpaid, 5: Trialing
  stripe_subscription_id?: string;
  paypal_subscription_id?: string;
  razorpay_subscription_id?: string;
  current_period_start?: string;
  current_period_end?: string;
  cancel_at_period_end: boolean;
  created_at: string;
  updated_at: string;
}

export interface Affiliate {
  id: number;
  name: string;
  email: string;
  commission_rate: number; // percentage
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface Referral {
  id: number;
  affiliate_id: number;
  referred_email: string;
  order_id?: number;
  subscription_id?: number;
  commission_earned: number;
  created_at: string;
}

export interface UpsellOffer {
  id: number;
  name: string;
  description: string;
  product_id: number;
  trigger_product_id: number;
  discount_percentage: number;
  is_active: boolean;
  created_at: string;
  updated_at: string;
}

export interface RevenueAnalytics {
  total_revenue: number;
  total_orders: number;
  total_subscriptions: number;
  total_affiliates: number;
  revenue_by_product: Array<{ product_name: string; revenue: number }>;
  monthly_revenue: Array<{ month: string; revenue: number }>;
}