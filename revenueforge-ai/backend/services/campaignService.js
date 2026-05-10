const Campaign = require('../models/Campaign');

class CampaignService {
  async createCampaign(campaignData) {
    const campaign = new Campaign(campaignData);
    return await campaign.save();
  }

  async getCampaignById(id) {
    return await Campaign.findById(id).populate('agency client', 'name email');
  }

  async getCampaignsByAgency(agencyId) {
    return await Campaign.find({ agency: agencyId }).populate('client', 'name email');
  }

  async getCampaignsByClient(clientId) {
    return await Campaign.find({ client: clientId }).populate('agency', 'name email');
  }

  async updateCampaign(id, updateData) {
    return await Campaign.findByIdAndUpdate(id, updateData, { new: true, runValidators: true });
  }

  async deleteCampaign(id) {
    return await Campaign.findByIdAndDelete(id);
  }

  async getAllCampaigns() {
    return await Campaign.find().populate('agency client', 'name email');
  }
}

module.exports = new CampaignService();