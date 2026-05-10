const mongoose = require('mongoose');

const revenueForecastSchema = new mongoose.Schema({
  agency: { type: mongoose.Schema.Types.ObjectId, ref: 'Agency', required: true },
  period: { 
    type: String, 
    enum: ['daily', 'weekly', 'monthly', 'quarterly', 'yearly'], 
    required: true 
  },
  startDate: { type: Date, required: true },
  endDate: { type: Date, required: true },
  predictedRevenue: { type: Number, required: true },
  actualRevenue: { type: Number, default: 0 },
  confidenceLevel: { type: Number, min: 0, max: 100, default: 80 },
  factors: [{ 
    name: { type: String, required: true },
    impact: { type: Number, min: -100, max: 100 }, // percentage impact
    description: { type: String }
  }],
  notes: { type: String },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('RevenueForecast', revenueForecastSchema);