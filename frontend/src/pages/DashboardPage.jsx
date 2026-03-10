import { useState, useEffect } from 'react';
import { fetchMedicaments } from '../api/medicamentsApi';
import { fetchAlertes } from '../api/medicamentsApi';
import { fetchVentes } from '../api/ventesApi';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorMessage from '../components/common/ErrorMessage';

function todayISO() {
  const d = new Date();
  return d.toISOString().slice(0, 10);
}

export default function DashboardPage() {
  const [stats, setStats] = useState({
    medicamentsCount: null,
    alertesCount: null,
    ventesAujourdhui: null,
  });
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      setLoading(true);
      setError(null);
      try {
        const today = todayISO();
        const [medData, alertes, ventesData] = await Promise.all([
          fetchMedicaments({}),
          fetchAlertes(),
          fetchVentes({ date_from: today, date_to: today }),
        ]);
        if (!cancelled) {
          setStats({
            medicamentsCount: medData.count ?? (medData.results?.length ?? 0),
            alertesCount: Array.isArray(alertes) ? alertes.length : 0,
            ventesAujourdhui: ventesData.count ?? (ventesData.results?.length ?? 0),
          });
        }
      } catch (err) {
        if (!cancelled) {
          setError(err.response?.data?.detail || err.message || 'Erreur lors du chargement');
        }
      } finally {
        if (!cancelled) setLoading(false);
      }
    };
    load();
    return () => { cancelled = true; };
  }, []);

  if (loading) return <LoadingSpinner />;
  if (error) return <ErrorMessage message={error} />;

  return (
    <div className="page dashboard-page">
      <h1>Dashboard</h1>
      <div className="dashboard-cards">
        <div className="card-stat">
          <span className="card-value">{stats.medicamentsCount ?? 0}</span>
          <span className="card-label">Médicaments</span>
        </div>
        <div className="card-stat card-alert">
          <span className="card-value">{stats.alertesCount ?? 0}</span>
          <span className="card-label">Alertes stock bas</span>
        </div>
        <div className="card-stat">
          <span className="card-value">{stats.ventesAujourdhui ?? 0}</span>
          <span className="card-label">Ventes du jour</span>
        </div>
      </div>
    </div>
  );
}
