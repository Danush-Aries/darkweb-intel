const express = require('express');
const router = express.Router();
const campaignController = require('../controllers/campaignController');

// Campaign routes
router.post('/', campaignController.createCampaign);
router.get('/', campaignController.getAllCampaigns);
router.get('/:id', campaignController.getCampaignById);
router.get('/agency/:agencyId', campaignController.getCampaignsByAgency);
router.get('/client/:clientId', campaignController.getCampaignsByClient);
router.put('/:id', campaignController.updateCampaign);
router.delete('/:id', campaignController.deleteCampaign);

module.exports = router;