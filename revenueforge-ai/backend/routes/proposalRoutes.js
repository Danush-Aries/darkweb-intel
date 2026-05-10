const express = require('express');
const router = express.Router();
const proposalController = require('../controllers/proposalController');

// Proposal routes
router.post('/', proposalController.createProposal);
router.get('/', proposalController.getAllProposals);
router.get('/:id', proposalController.getProposalById);
router.get('/agency/:agencyId', proposalController.getProposalsByAgency);
router.get('/client/:clientId', proposalController.getProposalsByClient);
router.put('/:id', proposalController.updateProposal);
router.delete('/:id', proposalController.deleteProposal);

module.exports = router;