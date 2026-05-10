const ContractService = require('../services/contractService');

exports.createContract = async (req, res) => {
  try {
    const contract = await ContractService.createContract(req.body);
    res.status(201).json(contract);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.getContractById = async (req, res) => {
  try {
    const contract = await ContractService.getContractById(req.params.id);
    if (!contract) {
      return res.status(404).json({ error: 'Contract not found' });
    }
    res.status(200).json(contract);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getContractsByAgency = async (req, res) => {
  try {
    const contracts = await ContractService.getContractsByAgency(req.params.agencyId);
    res.status(200).json(contracts);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getContractsByClient = async (req, res) => {
  try {
    const contracts = await ContractService.getContractsByClient(req.params.clientId);
    res.status(200).json(contracts);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.updateContract = async (req, res) => {
  try {
    const contract = await ContractService.updateContract(req.params.id, req.body);
    if (!contract) {
      return res.status(404).json({ error: 'Contract not found' });
    }
    res.status(200).json(contract);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.deleteContract = async (req, res) => {
  try {
    const contract = await ContractService.deleteContract(req.params.id);
    if (!contract) {
      return res.status(404).json({ error: 'Contract not found' });
    }
    res.status(200).json({ message: 'Contract deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getAllContracts = async (req, res) => {
  try {
    const contracts = await ContractService.getAllContracts();
    res.status(200).json(contracts);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};