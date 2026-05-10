const ProposalService = require('../services/proposalService');

exports.createProposal = async (req, res) => {
  try {
    const proposal = await ProposalService.createProposal(req.body);
    res.status(201).json(proposal);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.getProposalById = async (req, res) => {
  try {
    const proposal = await ProposalService.getProposalById(req.params.id);
    if (!proposal) {
      return res.status(404).json({ error: 'Proposal not found' });
    }
    res.status(200).json(proposal);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getProposalsByAgency = async (req, res) => {
  try {
    const proposals = await ProposalService.getProposalsByAgency(req.params.agencyId);
    res.status(200).json(proposals);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getProposalsByClient = async (req, res) => {
  try {
    const proposals = await ProposalService.getProposalsByClient(req.params.clientId);
    res.status(200).json(proposals);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.updateProposal = async (req, res) => {
  try {
    const proposal = await ProposalService.updateProposal(req.params.id, req.body);
    if (!proposal) {
      return res.status(404).json({ error: 'Proposal not found' });
    }
    res.status(200).json(proposal);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.deleteProposal = async (req, res) => {
  try {
    const proposal = await ProposalService.deleteProposal(req.params.id);
    if (!proposal) {
      return res.status(404).json({ error: 'Proposal not found' });
    }
    res.status(200).json({ message: 'Proposal deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getAllProposals = async (req, res) => {
  try {
    const proposals = await ProposalService.getAllProposals();
    res.status(200).json(proposals);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};