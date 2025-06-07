import { useState } from 'react';
import { Container, TextField, MenuItem, Button, Typography } from '@mui/material';

const restaurants = ['Pizza MTP', 'Tacos Deluxe', 'Vegan Bowl'];

export default function ClientPage() {
  const [form, setForm] = useState({
    nom: '',
    adresse: '',
    restaurant: restaurants[0],
    plat: '',
    heure: ''
  });

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const submit = async () => {
    await fetch('http://localhost:8000/orders', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(form)
    });
    alert('Commande envoy\u00e9e !');
    setForm({ nom: '', adresse: '', restaurant: restaurants[0], plat: '', heure: '' });
  };

  return (
    <Container sx={{ mt: 4 }}>
      <Typography variant="h4" gutterBottom>Passer une commande</Typography>
      <TextField label="Nom" name="nom" fullWidth margin="normal" value={form.nom} onChange={handleChange} />
      <TextField label="Adresse" name="adresse" fullWidth margin="normal" value={form.adresse} onChange={handleChange} />
      <TextField select label="Restaurant" name="restaurant" fullWidth margin="normal" value={form.restaurant} onChange={handleChange}>
        {restaurants.map(r => <MenuItem key={r} value={r}>{r}</MenuItem>)}
      </TextField>
      <TextField label="Plat" name="plat" fullWidth margin="normal" value={form.plat} onChange={handleChange} />
      <TextField label="Heure" name="heure" type="time" fullWidth margin="normal" value={form.heure} onChange={handleChange} />
      <Button variant="contained" onClick={submit} sx={{ mt: 2 }}>Envoyer</Button>
    </Container>
  );
}
