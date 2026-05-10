const Invoice = require('../models/Invoice');

class InvoiceService {
  async createInvoice(invoiceData) {
    const invoice = new Invoice(invoiceData);
    return await invoice.save();
  }

  async getInvoiceById(id) {
    return await Invoice.findById(id).populate('proposal client agency', 'title name email');
  }

  async getInvoicesByAgency(agencyId) {
    return await Invoice.find({ agency: agencyId }).populate('client proposal', 'name title');
  }

  async getInvoicesByClient(clientId) {
    return await Invoice.find({ client: clientId }).populate('agency proposal', 'firstName lastName title');
  }

  async updateInvoice(id, updateData) {
    return await Invoice.findByIdAndUpdate(id, updateData, { new: true, runValidators: true });
  }

  async deleteInvoice(id) {
    return await Invoice.findByIdAndDelete(id);
  }

  async getAllInvoices() {
    return await Invoice.find().populate('proposal client agency', 'title name email');
  }

  async markAsPaid(id) {
    return await Invoice.findByIdAndUpdate(id, { 
      status: 'paid', 
      paidDate: new Date() 
    }, { new: true });
  }

  async markAsOverdue(id) {
    return await Invoice.findByIdAndUpdate(id, { status: 'overdue' }, { new: true });
  }
}

module.exports = new InvoiceService();