const express = require('express');
const router = express.Router();
const teamController = require('../controllers/teamController');

// Team routes
router.post('/', teamController.createTeam);
router.get('/', teamController.getAllTeams); // This would need to be implemented
router.get('/:id', teamController.getTeamById);
router.get('/agency/:agencyId', teamController.getTeamsByAgency);
router.put('/:id', teamController.updateTeam);
router.delete('/:id', teamController.deleteTeam);

module.exports = router;