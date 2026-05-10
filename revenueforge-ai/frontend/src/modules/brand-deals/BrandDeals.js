import React from 'react';
import { Container, Typography, Card, CardContent, Button } from '@mui/material';

const BrandDeals = () => {
  return (
    <Container maxWidth="lg">
      <Typography variant="h4" gutterBottom mb={4}>
        Brand Deals
      </Typography>
      <Card>
        <CardContent>
          <Typography variant="h5">Manage your brand partnerships</Typography>
          <Typography variant="body2" color="text.secondary">
            Track negotiations, contracts, deliverables, and payments.
          </Typography>
          <Button variant="contained" color="primary" size="large">
            Create New Brand Deal
          </Button>
        </CardContent>
      </Card>
    </Container>
  );
};

export default BrandDeals;
