import React, { useState } from 'react';
import { Button, TextField, Select, MenuItem, FormControl, InputLabel, Box, Typography, Paper } from '@mui/material';
import axios from 'axios';

const InvoiceForm = () => {
  const [formData, setFormData] = useState({
    proposal: '',
    client: '',
    agency: '',
    invoiceNumber: '',
    amount: '',
    taxAmount: 0,
    totalAmount: '',
    status: 'draft',
    dueDate: '',
    lineItems: [{ description: '', quantity: 1, unitPrice: 0, total: 0 }]
  });
  const [proposals, setProposals] = useState([]);
  const [clients, setClients] = useState([]);
  const [agencies, setAgencies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchProposals();
    fetchClients();
    fetchAgencies();
  }, []);

  const fetchProposals = async () => {
    try {
      const response = await axios.get('/api/proposals');
      setProposals(response.data);
    } catch (err) {
      console.error('Error fetching proposals:', err);
    }
  };

  const fetchClients = async () => {
    try {
      const response = await axios.get('/api/clients');
      setClients(response.data);
    } catch (err) {
      console.error('Error fetching clients:', err);
    }
  };

  const fetchAgencies = async () => {
    try {
      const response = await axios.get('/api/agencies');
      setAgencies(response.data);
    } catch (err) {
      console.error('Error fetching agencies:', err);
    }
  };

  const handleChange = (e) => {
    const { name, value } = e.target;
    setFormData(prev => ({
      ...prev,
      [name]: value
    }));
  };

  const handleLineItemChange = (index, field, value) => {
    setFormData(prev => {
      const lineItems = [...prev.lineItems];
      lineItems[index][field] = value;
      return { ...prev, lineItems };
    });
  };

  const addLineItem = () => {
    setFormData(prev => ({
      ...prev,
      lineItems: [...prev.lineItems, { description: '', quantity: 1, unitPrice: 0, total: 0 }]
    }));
  };

  const removeLineItem = (index) => {
    setFormData(prev => {
      const lineItems = [...prev.lineItems];
      lineItems.splice(index, 1);
      return { ...prev, lineItems };
    });
  };

  const calculateTotal = () => {
    return formData.lineItems.reduce((sum, item) => sum + (item.quantity * item.unitPrice), 0);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      // Calculate total from line items
      const totalAmount = calculateTotal();
      const invoiceData = {
        ...formData,
        totalAmount,
        taxAmount: formData.taxAmount || 0
      };
      await axios.post('/api/invoices', invoiceData);
      // Reset form
      setFormData({
        proposal: '',
        client: '',
        agency: '',
        invoiceNumber: '',
        amount: '',
        taxAmount: 0,
        totalAmount: '',
        status: 'draft',
        dueDate: '',
        lineItems: [{ description: '', quantity: 1, unitPrice: 0, total: 0 }]
      });
      alert('Invoice created successfully!');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create invoice');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Create New Invoice
      </Typography>
      {error && (
        <Typography color="error">
          {error}
        </Typography>
      )}
      <form onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <FormControl fullWidth>
          <InputLabel id="proposal-label">Proposal</InputLabel>
          <Select
            labelId="proposal-label"
            label="Proposal"
            name="proposal"
            value={formData.proposal}
            onChange={handleChange}
            required
          >
            <MenuItem value="">-- Select Proposal --</MenuItem>
            {proposals.map(proposal => (
              <MenuItem key={proposal._id} value={proposal._id}>
                {proposal.title}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl fullWidth>
          <InputLabel id="client-label">Client</InputLabel>
          <Select
            labelId="client-label"
            label="Client"
            name="client"
            value={formData.client}
            onChange={handleChange}
            required
          >
            <MenuItem value="">-- Select Client --</MenuItem>
            {clients.map(client => (
              <MenuItem key={client._id} value={client._id}>
                {client.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <FormControl fullWidth>
          <InputLabel id="agency-label">Agency</InputLabel>
          <Select
            labelId="agency-label"
            label="Agency"
            name="agency"
            value={formData.agency}
            onChange={handleChange}
            required
          >
            <MenuItem value="">-- Select Agency --</MenuItem>
            {agencies.map(agency => (
              <MenuItem key={agency._id} value={agency._id}>
                {agency.name}
              </MenuItem>
            ))}
          </Select>
        </FormControl>
        <TextField
          label="Invoice Number"
          name="invoiceNumber"
          value={formData.invoiceNumber}
          onChange={handleChange}
          required
          fullWidth
        />
        <TextField
          label="Amount (will be calculated from line items)"
          name="amount"
          value={formData.amount}
          onChange={handleChange}
          fullWidth
          InputProps={{ readOnly: true }}
        />
        <TextField
          label="Tax Amount"
          name="taxAmount"
          type="number"
          value={formData.taxAmount}
          onChange={handleChange}
          fullWidth
        />
        <TextField
          label="Total Amount"
          name="totalAmount"
          value={formData.totalAmount}
          onChange={handleChange}
          fullWidth
          InputProps={{ readOnly: true }}
        />
        <FormControl fullWidth>
          <InputLabel id="status-label">Status</InputLabel>
          <Select
            labelId="status-label"
            label="Status"
            name="status"
            value={formData.status}
            onChange={handleChange}
          >
            <MenuItem value="draft">Draft</MenuItem>
            <MenuItem value="sent">Sent</MenuItem>
            <MenuItem value="paid">Paid</MenuItem>
            <MenuItem value="overdue">Overdue</MenuItem>
            <MenuItem value="cancelled">Cancelled</MenuItem>
          </Select>
        </FormControl>
        <TextField
          label="Due Date"
          name="dueDate"
          type="date"
          value={formData.dueDate}
          onChange={handleChange}
          required
          fullWidth
        />
        <Typography variant="h6" gutterBottom>
          Line Items
        </Typography>
        {formData.lineItems.map((item, index) => (
          <Paper key={index} sx={{ p: 2, border: 1, borderColor: 'divider' }}>
            <Box sx={{ display: 'flex', gap: 2, mb: 1 }}>
              <TextField
                label="Description"
                name={`lineItems[${index}][description]`}
                value={item.description}
                onChange={(e) => handleLineItemChange(index, 'description', e.target.value)}
                flexGrow
              />
              <TextField
                label="Quantity"
                type="number"
                name={`lineItems[${index}][quantity]`}
                value={item.quantity}
                onChange={(e) => handleLineItemChange(index, 'quantity', parseInt(e.target.value) || 1)}
                sx={{ width: 80 }}
              />
              <TextField
                label="Unit Price"
                type="number"
                name={`lineItems[${index}][unitPrice]`}
                value={item.unitPrice}
                onChange={(e) => handleLineItemChange(index, 'unitPrice', parseFloat(e.target.value) || 0)}
                sx={{ width: 100 }}
              />
              <TextField
                label="Total"
                name={`lineItems[${index}][total]`}
                value={item.total}
                onChange={(e) => handleLineItemChange(index, 'total', parseFloat(e.target.value) || 0)}
                sx={{ width: 100 }}
                InputProps={{ readOnly: true }}
              />
            </Box>
            <Button
              variant="outlined"
              color="error"
              size="small"
              onClick={() => removeLineItem(index)}
              sx={{ alignSelf: 'flex-end' }}
            >
              Remove
            </Button>
          </Paper>
        ))}
        <Button
          variant="outlined"
          color="primary"
          size="small"
          onClick={addLineItem}
          sx={{ mt: 1 }}
        >
          Add Line Item
        </Button>
        <Button 
          type="submit" 
          variant="contained" 
          color="primary"
          disabled={loading}
          sx={{ mt: 2 }}
        >
          {loading ? 'Creating...' : 'Create Invoice'}
        </Button>
      </form>
    </Box>
  );
};

export default InvoiceForm;