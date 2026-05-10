const mongoose = require('mongoose');

const contractSchema = new mongoose.Schema({
  title: { type: String, required: true },
  proposal: { type: mongoose.Schema.Types.ObjectId, ref: 'Proposal' },
  client: { type: mongoose.Schema.Types.ObjectId, ref: 'Client', required: true },
  agency: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  terms: { type: String, required: true },
  deliverables: [{ type: String }],
  timeline: { type: String },
  paymentTerms: { type: String },
  status: { 
    type: String, 
    enum: ['draft', 'sent', 'signed', 'revoked', 'expired'], 
    default: 'draft' 
  },
  signedAt: { type: Date },
  expiresAt: { type: Date },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Contract', contractSchema);