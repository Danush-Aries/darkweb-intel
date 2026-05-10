const Client = require('../models/Client');

class ClientService {
  async createClient(clientData) {
    const client = new Client(clientData);
    return await client.save();
  }

  async getClientById(id) {
    return await Client.findById(id);
  }

  async getAllClients() {
    return await Client.find();
  }

  async updateClient(id, updateData) {
    return await Client.findByIdAndUpdate(id, updateData, { new: true, runValidators: true });
  }

  async deleteClient(id) {
    return await Client.findByIdAndDelete(id);
  }

  async searchClients(query) {
    return await Client.find({
      $or: [
        { name: { $regex: query, $options: 'i' } },
        { email: { $regex: query, $options: 'i' } },
        { company: { $regex: query, $options: 'i' } }
      ]
    });
  }
}

module.exports = new ClientService();