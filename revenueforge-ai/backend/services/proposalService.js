const Proposal = require('../models/Proposal');

class ProposalService {
  async createProposal(proposalData) {
    const proposal = new Proposal(proposalData);
    return await proposal.save();
  }

  async getProposalById(id) {
    return await Proposal.findById(id).populate('client agency', 'name email');
  }

  async getProposalsByAgency(agencyId) {
    return await Proposal.find({ agency: agencyId }).populate('client', 'name email');
  }

  async getProposalsByClient(clientId) {
    return await Proposal.find({ client: clientId }).populate('agency', 'firstName lastName');
  }

  async updateProposal(id, updateData) {
    return await Proposal.findByIdAndUpdate(id, updateData, { new: true, runValidators: true });
  }

  async deleteProposal(id) {
    return await Proposal.findByIdAndDelete(id);
  }

  async getAllProposals() {
    return await Proposal.find().populate('client agency', 'name email');
  }
}

module.exports = new ProposalService();