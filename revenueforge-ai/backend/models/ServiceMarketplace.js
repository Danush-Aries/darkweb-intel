const mongoose = require('mongoose');

const serviceMarketplaceSchema = new mongoose.Schema({
  name: { type: String, required: true },
  description: { type: String },
  category: { type: String, required: true },
  subcategory: { type: String },
  provider: { type: String, required: true }, // e.g., Fiverr, Upwork, Specialist agencies
  pricing: {
    type: { type: String, enum: ['fixed', 'hourly', 'retainer', 'performance'] },
    amount: { type: Number },
    currency: { type: String, default: 'USD' }
  },
  rating: { type: Number, min: 0, max: 5, default: 0 },
  reviewCount: { type: Number, default: 0 },
  deliveryTime: { type: String }, // e.g., "3 days", "1 week"
  revisions: { type: Number },
  features: [{ type: String }],
  requirements: [{ type: String }],
  gallery: [{ type: String }], // URLs to images/videos
  isActive: { type: Boolean, default: true },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('ServiceMarketplace', serviceMarketplaceSchema);