const express = require('express');
const router = express.Router();
const clientController = require('../controllers/clientController');

// Client routes
router.post('/', clientController.createClient);
router.get('/', clientController.getAllClients);
router.get('/:id', clientController.getClientById);
router.put('/:id', clientController.updateClient);
router.delete('/:id', clientController.deleteClient);
router.get('/search/:query', clientController.searchClients);

module.exports = router;