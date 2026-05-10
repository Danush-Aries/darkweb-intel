const TeamService = require('../services/teamService');

exports.createTeam = async (req, res) => {
  try {
    const team = await TeamService.createTeam(req.body);
    res.status(201).json(team);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.getTeamById = async (req, res) => {
  try {
    const team = await TeamService.getTeamById(req.params.id);
    if (!team) {
      return res.status(404).json({ error: 'Team not found' });
    }
    res.status(200).json(team);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.getTeamsByAgency = async (req, res) => {
  try {
    const teams = await TeamService.getTeamsByAgency(req.params.agencyId);
    res.status(200).json(teams);
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};

exports.updateTeam = async (req, res) => {
  try {
    const team = await TeamService.updateTeam(req.params.id, req.body);
    if (!team) {
      return res.status(404).json({ error: 'Team not found' });
    }
    res.status(200).json(team);
  } catch (error) {
    res.status(400).json({ error: error.message });
  }
};

exports.deleteTeam = async (req, res) => {
  try {
    const team = await TeamService.deleteTeam(req.params.id);
    if (!team) {
      return res.status(404).json({ error: 'Team not found' });
    }
    res.status(200).json({ message: 'Team deleted successfully' });
  } catch (error) {
    res.status(500).json({ error: error.message });
  }
};