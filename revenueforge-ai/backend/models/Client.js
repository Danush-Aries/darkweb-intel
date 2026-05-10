const mongoose = require('mongoose');

const clientSchema = new mongoose.Schema({
  name: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  phone: { type: String },
  address: { type: String },
  company: { type: String },
  website: { type: String },
  industry: { type: String },
  status: { 
    type: String, 
    enum: ['lead', 'active', 'inactive', 'churned'], 
    default: 'lead' 
  },
  tags: [{ type: String }],
  notes: { type: String },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Client', clientSchema);