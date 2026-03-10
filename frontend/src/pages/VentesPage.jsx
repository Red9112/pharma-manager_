import { useState, useEffect } from 'react';
import { useVentes } from '../hooks/useVentes';
import { fetchMedicaments } from '../api/medicamentsApi';
import { createVente, getVente, annulerVente } from '../api/ventesApi';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorMessage from '../components/common/ErrorMessage';
import VenteForm from '../components/ventes/VenteForm';

const STATUT_LABEL = { en_cours: 'En cours', completee: 'Complétée', annulee: 'Annulée' };

export default function VentesPage() {
  const [dateFrom, setDateFrom] = useState('');
  const [dateTo, setDateTo] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [medicaments, setMedicaments] = useState([]);
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState(null);
  const [detailVente, setDetailVente] = useState(null);

  const filters = { date_from: dateFrom || undefined, date_to: dateTo || undefined };
  const { ventes, loading, error, refetch } = useVentes(filters);

  useEffect(() => {
    let cancelled = false;
    const load = async () => {
      try {
        const data = await fetchMedicaments({});
        if (!cancelled) setMedicaments(data.results ?? []);
      } catch {
        if (!cancelled) setMedicaments([]);
      }
    };
    load();
    return () => { cancelled = true; };
  }, []);

  const handleCreateVente = async (payload) => {
    setSaving(true);
    setFormError(null);
    try {
      await createVente(payload);
      setShowForm(false);
      refetch();
    } catch (err) {
      const msg = err.response?.data
        ? (typeof err.response.data === 'object' && err.response.data.detail
            ? err.response.data.detail
            : JSON.stringify(err.response.data))
        : err.message;
      setFormError(msg);
    } finally {
      setSaving(false);
    }
  };

  const openDetail = async (v) => {
    try {
      const full = await getVente(v.id);
      setDetailVente(full);
    } catch (err) {
      alert(err.response?.data?.detail || err.message);
    }
  };

  const handleAnnuler = async (id) => {
    if (!window.confirm('Annuler cette vente ? Le stock sera réintégré.')) return;
    try {
      await annulerVente(id);
      setDetailVente(null);
      refetch();
    } catch (err) {
      alert(err.response?.data?.detail || err.message);
    }
  };

  return (
    <div className="page ventes-page">
      <header className="page-header">
        <h1>Ventes</h1>
        <button type="button" className="btn-primary" onClick={() => { setShowForm(true); setFormError(null); }}>
          Nouvelle vente
        </button>
      </header>

      <div className="filters">
        <label>
          Du <input type="date" value={dateFrom} onChange={(e) => setDateFrom(e.target.value)} />
        </label>
        <label>
          Au <input type="date" value={dateTo} onChange={(e) => setDateTo(e.target.value)} />
        </label>
      </div>

      {loading && <LoadingSpinner />}
      {error && <ErrorMessage message={error} onRetry={refetch} />}

      {!loading && !error && (
        <>
          <p className="count">{ventes.length > 0 ? `${ventes.length} vente(s)` : 'Aucune vente.'}</p>
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Référence</th>
                  <th>Date</th>
                  <th>Total TTC</th>
                  <th>Statut</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {ventes.map((v) => (
                  <tr key={v.id}>
                    <td>{v.reference}</td>
                    <td>{v.date_vente ? new Date(v.date_vente).toLocaleString('fr-FR') : '—'}</td>
                    <td>{Number(v.total_ttc).toFixed(2)}</td>
                    <td>
                      <span className={`badge badge-${v.statut === 'annulee' ? 'danger' : 'info'}`}>
                        {STATUT_LABEL[v.statut] ?? v.statut}
                      </span>
                    </td>
                    <td>
                      <button type="button" className="btn-sm" onClick={() => openDetail(v)}>Détail</button>
                      {v.statut !== 'annulee' && (
                        <button type="button" className="btn-sm btn-danger" onClick={() => handleAnnuler(v.id)}>
                          Annuler
                        </button>
                      )}
                    </td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        </>
      )}

      {showForm && (
        <div className="modal-overlay" onClick={() => setShowForm(false)}>
          <div className="modal modal-wide" onClick={(e) => e.stopPropagation()}>
            <h2>Nouvelle vente</h2>
            {formError && <ErrorMessage message={formError} />}
            <VenteForm
              medicaments={medicaments}
              onSubmit={handleCreateVente}
              onCancel={() => setShowForm(false)}
              saving={saving}
            />
          </div>
        </div>
      )}

      {detailVente && (
        <div className="modal-overlay" onClick={() => setDetailVente(null)}>
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>Vente {detailVente.reference}</h2>
            <p><strong>Date :</strong> {detailVente.date_vente ? new Date(detailVente.date_vente).toLocaleString('fr-FR') : '—'}</p>
            <p><strong>Total TTC :</strong> {Number(detailVente.total_ttc).toFixed(2)}</p>
            <p><strong>Statut :</strong> {STATUT_LABEL[detailVente.statut] ?? detailVente.statut}</p>
            {detailVente.notes && <p><strong>Notes :</strong> {detailVente.notes}</p>}
            {detailVente.lignes && detailVente.lignes.length > 0 && (
              <table className="data-table">
                <thead>
                  <tr><th>Médicament</th><th>Qté</th><th>Prix unit.</th><th>Sous-total</th></tr>
                </thead>
                <tbody>
                  {detailVente.lignes.map((l) => (
                    <tr key={l.id}>
                      <td>{l.medicament_nom ?? `Médicament #${l.medicament}`}</td>
                      <td>{l.quantite}</td>
                      <td>{Number(l.prix_unitaire).toFixed(2)}</td>
                      <td>{Number(l.sous_total).toFixed(2)}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
            <div className="form-actions" style={{ marginTop: '1rem' }}>
              {detailVente.statut !== 'annulee' && (
                <button type="button" className="btn-danger" onClick={() => handleAnnuler(detailVente.id)}>Annuler la vente</button>
              )}
              <button type="button" onClick={() => setDetailVente(null)}>Fermer</button>
            </div>
          </div>
        </div>
      )}
    </div>
  );
}
