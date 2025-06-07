import { useState, useEffect } from 'react';
import { Container, Typography, MenuItem, TextField, List, ListItem } from '@mui/material';

const restaurants = ['Pizza MTP', 'Tacos Deluxe', 'Vegan Bowl'];

export default function RestaurantPage() {
  const [selected, setSelected] = useState(restaurants[0]);
  const [orders, setOrders] = useState([]);

  useEffect(() => { fetchOrders(); }, [selected]);

  const fetchOrders = async () => {
    const res = await fetch('http://localhost:8000/orders');
    const data = await res.json();
    setOrders(data.filter(o => o.restaurant === selected));
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Commandes du restaurant</Typography>
      <TextField select label="Restaurant" value={selected} onChange={e => setSelected(e.target.value)} sx={{ mb: 2 }}>
        {restaurants.map(r => <MenuItem key={r} value={r}>{r}</MenuItem>)}
      </TextField>
      <List>
        {orders.map(o => (
          <ListItem key={o.id}>{`${o.plat} pour ${o.nom} \u00e0 ${o.heure} - Coursier: ${o.coursier || 'Aucun'}`}</ListItem>
        ))}
      </List>
    </Container>
  );
}
