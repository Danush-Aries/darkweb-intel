const Agency = require('../models/Agency');

class AgencyService {
  async createAgency(agencyData) {
    const agency = new Agency(agencyData);
    return await agency.save();
  }

  async getAgencyById(id) {
    return await Agency.findById(id);
  }

  async getAllAgencies() {
    return await Agency.find();
  }

  async updateAgency(id, updateData) {
    return await Agency.findByIdAndUpdate(id, updateData, { new: true, runValidators: true });
  }

  async deleteAgency(id) {
    return await Agency.findByIdAndDelete(id);
  }
}

module.exports = new AgencyService();