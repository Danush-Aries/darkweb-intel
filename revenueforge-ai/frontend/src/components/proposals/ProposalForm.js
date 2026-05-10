import React, { useState, useEffect } from 'react';
import { Button, TextField, Select, MenuItem, FormControl, InputLabel, Box, Typography, Paper } from '@mui/material';
import axios from 'axios';

const ProposalForm = () => {
  const [formData, setFormData] = useState({
    title: '',
    client: '',
    agency: '',
    services: [],
    deliverables: [],
    timeline: '',
    budget: '',
    status: 'draft'
  });
  const [clients, setClients] = useState([]);
  const [agencies, setAgencies] = useState([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  useEffect(() => {
    fetchClients();
    fetchAgencies();
  }, []);

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

  const handleSubmit = async (e) => {
    e.preventDefault();
    setLoading(true);
    try {
      await axios.post('/api/proposals', formData);
      // Reset form
      setFormData({
        title: '',
        client: '',
        agency: '',
        services: [],
        deliverables: [],
        timeline: '',
        budget: '',
        status: 'draft'
      });
      alert('Proposal created successfully!');
    } catch (err) {
      setError(err.response?.data?.error || 'Failed to create proposal');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Box sx={{ p: 4 }}>
      <Typography variant="h4" gutterBottom>
        Create New Proposal
      </Typography>
      {error && (
        <Typography color="error">
          {error}
        </Typography>
      )}
      <form onSubmit={handleSubmit} sx={{ display: 'flex', flexDirection: 'column', gap: 2 }}>
        <TextField
          label="Title"
          name="title"
          value={formData.title}
          onChange={handleChange}
          required
          fullWidth
        />
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
          label="Services (comma separated)"
          name="services"
          value={formData.services.join(', ')}
          onChange={(e) => setFormData(prev => ({
            ...prev,
            services: e.target.value.split(',').map(s => s.trim()).filter(Boolean)
          }))]
          fullWidth
        />
        <TextField
          label="Deliverables (comma separated)"
          name="deliverables"
          value={formData.deliverables.join(', ')}
          onChange={(e) => setFormData(prev => ({
            ...prev,
            deliverables: e.target.value.split(',').map(d => d.trim()).filter(Boolean)
          }))]
          fullWidth
        />
        <TextField
          label="Timeline"
          name="timeline"
          value={formData.timeline}
          onChange={handleChange}
          fullWidth
        />
        <TextField
          label="Budget"
          name="budget"
          type="number"
          value={formData.budget}
          onChange={handleChange}
          required
          fullWidth
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
            <MenuItem value="accepted">Accepted</MenuItem>
            <MenuItem value="rejected">Rejected</MenuItem>
            <MenuItem value="expired">Expired</MenuItem>
          </Select>
        </FormControl>
        <Button 
          type="submit" 
          variant="contained" 
          color="primary"
          disabled={loading}
          sx={{ mt: 2 }}
        >
          {loading ? 'Creating...' : 'Create Proposal'}
        </Button>
      </form>
    </Box>
  );
};

export default ProposalForm;