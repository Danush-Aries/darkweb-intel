const AgencyService = require('../services/agencyService');

exports.createAgency = async (req, res) => {
  try {
    const agency = await AgencyService.createAgency(req.body);
    res.status(201).json(agency);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.getAgencyById = async (req, res) => {
  try {
    const agency = await AgencyService.getAgencyById(req.params.id);
    if (!agency) {
      return res.status(404).json({ error: 'Agency not found' });
    }
    res.status(200).json(agency);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getAllAgencies = async (req, res) => {
  try {
    const agencies = await AgencyService.getAllAgencies();
    res.status(200).json(agencies);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.updateAgency = async (req, res) => {
  try {
    const agency = await AgencyService.updateAgency(req.params.id, req.body);
    if (!agency) {
      return res.status(404).json({ error: 'Agency not found' });
    }
    res.status(200).json(agency);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.deleteAgency = async (req, res) => {
  try {
    const agency = await AgencyService.deleteAgency(req.params.id);
    if (!agency) {
      return res.status(404).json({ error: 'Agency not found' });
    }
    res.status(200).json({ message: 'Agency deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};