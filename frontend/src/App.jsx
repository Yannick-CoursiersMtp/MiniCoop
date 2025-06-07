import { BrowserRouter as Router, Routes, Route, Link } from 'react-router-dom';
import { AppBar, Toolbar, Button } from '@mui/material';
import ClientPage from './pages/ClientPage.jsx';
import RestaurantPage from './pages/RestaurantPage.jsx';
import CourierPage from './pages/CourierPage.jsx';
import AdminPage from './pages/AdminPage.jsx';

export default function App() {
  return (
    <Router>
      <AppBar position="static">
        <Toolbar>
          <Button color="inherit" component={Link} to="/client">Client</Button>
          <Button color="inherit" component={Link} to="/restaurant">Restaurant</Button>
          <Button color="inherit" component={Link} to="/courier">Courier</Button>
          <Button color="inherit" component={Link} to="/admin">Admin</Button>
        </Toolbar>
      </AppBar>
      <Routes>
        <Route path="/client" element={<ClientPage />} />
        <Route path="/restaurant" element={<RestaurantPage />} />
        <Route path="/courier" element={<CourierPage />} />
        <Route path="/admin" element={<AdminPage />} />
        <Route path="/" element={<ClientPage />} />
      </Routes>
    </Router>
  );
}
