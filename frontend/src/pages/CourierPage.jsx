import { useState } from 'react';
import { Container, TextField, Button, List, ListItem, Typography } from '@mui/material';

export default function CourierPage() {
  const [name, setName] = useState('');
  const [orders, setOrders] = useState([]);

  const fetchOrders = async () => {
    const res = await fetch('http://localhost:8000/orders');
    const data = await res.json();
    setOrders(data.filter(o => o.coursier === name));
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Mes livraisons</Typography>
      <TextField label="Nom" value={name} onChange={e => setName(e.target.value)} sx={{ mb: 2 }} />
      <Button variant="contained" onClick={fetchOrders}>Voir mes livraisons</Button>
      <List>
        {orders.map(o => (
          <ListItem key={o.id}>{`${o.plat} pour ${o.nom} \u00e0 ${o.adresse} \u00e0 ${o.heure}`}</ListItem>
        ))}
      </List>
    </Container>
  );
}
