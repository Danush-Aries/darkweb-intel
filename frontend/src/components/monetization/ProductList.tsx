import React, { useState, useEffect } from 'react';
import { monetizationService } from '@/src/lib/monetizationService';
import { Product } from '@/src/types/monetization-types';

export default function ProductList() {
  const [products, setProducts] = useState<Product[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
    const fetchProducts = async () => {
      try {
        setLoading(true);
        const data = await monetizationService.getProducts();
        setProducts(data);
      } catch (err) {
        setError('Failed to load products');
        console.error(err);
      } finally {
        setLoading(false);
      }
    };

    fetchProducts();
  }, []);

  if (loading) return <div className="text-center py-8">Loading products...</div>;
  if (error) return <div className="text-center text-red-500 py-8">{error}</div>;

  return (
    <div className="space-y-6">
      {products.length === 0 ? (
        <p className="text-center text-gray-500">No products available.</p>
      ) : (
        <div className="grid gap-4 md:grid-cols-2 lg:grid-cols-3">
          {products.map((product) => (
            <div key={product.id} className="bg-slate-800 rounded-lg p-6 hover:shadow-lg transition-shadow">
              <h3 className="text-xl font-semibold mb-2">{product.name}</h3>
              <p className="text-gray-400 mb-4 line-clamp-3">{product.description}</p>
              <div className="flex items-baseline mb-4">
                <span className="text-2xl font-bold text-green-400">
                  {product.price} {product.currency}
                </span>
                {product.billing_interval && (
                  <span className="ml-3 text-sm text-gray-500">/{product.billing_interval}</span>
                )}
              </div>
              <div className="mt-auto">
                {/* In a real app, we would have a button to buy or subscribe */}
                <button
                  onClick={() => alert('Purchase functionality would be implemented here')}
                  className="w-full px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700 disabled:opacity-50"
                  disabled
                >
                  {product.product_type === 3 || product.product_type === 4 ? 'Subscribe' : 'Buy Now'}
                </button>
              </div>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}