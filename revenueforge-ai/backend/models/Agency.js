const mongoose = require('mongoose');

const agencySchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  phone: { type: String },
  address: { type: String },
  website: { type: String },
  industry: { type: String },
  logo: { type: String },
  timezone: { type: String, default: 'UTC' },
  currency: { type: String, default: 'USD' },
  status: { 
    type: String, 
    enum: ['active', 'suspended', 'cancelled'], 
    default: 'active' 
  },
  plan: { 
    type: String, 
    enum: ['free', 'pro', 'enterprise'], 
    default: 'free' 
  },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Agency', agencySchema);