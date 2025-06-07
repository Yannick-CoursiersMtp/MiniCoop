import { useState, useEffect } from 'react';
import { Container, Typography, TextField, Button, List, ListItem } from '@mui/material';

export default function AdminPage() {
  const [orders, setOrders] = useState([]);
  const [assignments, setAssignments] = useState({});

  useEffect(() => { fetchOrders(); }, []);

  const fetchOrders = async () => {
    const res = await fetch('http://localhost:8000/orders');
    setOrders(await res.json());
  };

  const assign = async (id) => {
    const coursier = assignments[id] ?? '';
    await fetch(`http://localhost:8000/orders/${id}/assign`, {
      method: 'PUT',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ coursier })
    });
    fetchOrders();
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Gestion des commandes</Typography>
      <List>
        {orders.map(o => (
          <ListItem key={o.id} sx={{ flexDirection: 'column', alignItems: 'flex-start' }}>
            <Typography>{`${o.plat} pour ${o.nom} (${o.restaurant}) \u00e0 ${o.heure}`}</Typography>
            <TextField
              label="Coursier"
              value={assignments[o.id] ?? o.coursier ?? ''}
              onChange={e => setAssignments(prev => ({ ...prev, [o.id]: e.target.value }))}
              sx={{ mr: 1, mt: 1 }}
            />
            <Button variant="contained" onClick={() => assign(o.id)} sx={{ mt: 1 }}>Assigner</Button>
          </ListItem>
        ))}
      </List>
    </Container>
  );
}
