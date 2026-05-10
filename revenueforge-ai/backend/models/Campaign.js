const mongoose = require('mongoose');

const campaignSchema = new mongoose.Schema({
  name: { type: String, required: true },
  description: { type: String },
  agency: { type: mongoose.Schema.Types.ObjectId, ref: 'Agency', required: true },
  client: { type: mongoose.Schema.Types.ObjectId, ref: 'Client', required: true },
  startDate: { type: Date, required: true },
  endDate: { type: Date },
  status: { 
    type: String, 
    enum: ['planning', 'active', 'paused', 'completed', 'cancelled'], 
    default: 'planning' 
  },
  budget: { type: Number },
  actualSpend: { type: Number, default: 0 },
  objectives: [{ type: String }],
  KPIs: [{ 
    name: { type: String, required: true },
    target: { type: Number },
    current: { type: Number, default: 0 }
  }],
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Campaign', campaignSchema);