import { BrowserRouter, Routes, Route, NavLink } from 'react-router-dom';
import MedicamentsPage from './pages/MedicamentsPage';
import VentesPage from './pages/VentesPage';
import DashboardPage from './pages/DashboardPage';
import './App.css';

function App() {
  return (
    <BrowserRouter>
      <div className="app">
        <nav className="nav">
          <NavLink to="/" end className={({ isActive }) => (isActive ? 'active' : '')}>
            Dashboard
          </NavLink>
          <NavLink to="/medicaments" className={({ isActive }) => (isActive ? 'active' : '')}>
            Médicaments
          </NavLink>
          <NavLink to="/ventes" className={({ isActive }) => (isActive ? 'active' : '')}>
            Ventes
          </NavLink>
        </nav>
        <main className="main">
          <Routes>
            <Route path="/" element={<DashboardPage />} />
            <Route path="/medicaments" element={<MedicamentsPage />} />
            <Route path="/ventes" element={<VentesPage />} />
          </Routes>
        </main>
      </div>
    </BrowserRouter>
  );
}

export default App;
