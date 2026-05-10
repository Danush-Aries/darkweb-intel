const mongoose = require('mongoose');

const proposalSchema = new mongoose.Schema({
  title: { type: String, required: true },
  client: { type: mongoose.Schema.Types.ObjectId, ref: 'Client', required: true },
  agency: { type: mongoose.Schema.Types.ObjectId, ref: 'User', required: true },
  services: [{ type: String }],
  deliverables: [{ type: String }],
  timeline: { type: String },
  budget: { type: Number, required: true },
  status: { 
    type: String, 
    enum: ['draft', 'sent', 'accepted', 'rejected', 'expired'], 
    default: 'draft' 
  },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('Proposal', proposalSchema);