import React from 'react';
import { Container, Typography, Card, CardContent, Button } from '@mui/material';

const Sponsorships = () => {
  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom mb={4}>
        Sponsorship Tracking
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="h5">Track and manage sponsorships</Typography>
          <Typography variant="body2" color="text.secondary">
            Monitor performance, payments, and deliverables for sponsorship deals.
          </Typography>
          <Button variant="contained" color="primary" size="large">
            Create New Sponsorship
          </Button>
        </CardContent>
      </Card>
    </Container>
  );
};

export default Sponsorships;
