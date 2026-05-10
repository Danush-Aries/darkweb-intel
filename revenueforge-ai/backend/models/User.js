const mongoose = require('mongoose');

const userSchema = new mongoose.Schema({
  firstName: { type: String, required: true },
  lastName: { type: String, required: true },
  email: { type: String, required: true, unique: true },
  password: { type: String, required: true },
  role: { 
    type: String, 
    enum: ['admin', 'agency_owner', 'team_member', 'accountant'], 
    default: 'team_member' 
  },
  agency: { type: mongoose.Schema.Types.ObjectId, ref: 'Agency' },
  team: { type: mongoose.Schema.Types.ObjectId, ref: 'Team' },
  isActive: { type: Boolean, default: true },
  createdAt: { type: Date, default: Date.now },
  updatedAt: { type: Date, default: Date.now }
});

module.exports = mongoose.model('User', userSchema);