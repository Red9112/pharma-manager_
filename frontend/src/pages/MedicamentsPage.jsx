import { useState, useCallback } from 'react';
import { useMedicaments } from '../hooks/useMedicaments';
import { useCategories } from '../hooks/useCategories';
import { createMedicament, updateMedicament, deleteMedicament } from '../api/medicamentsApi';
import LoadingSpinner from '../components/common/LoadingSpinner';
import ErrorMessage from '../components/common/ErrorMessage';
import MedicamentForm from '../components/medicaments/MedicamentForm';

export default function MedicamentsPage() {
  const [search, setSearch] = useState('');
  const [categorie, setCategorie] = useState('');
  const [showForm, setShowForm] = useState(false);
  const [editing, setEditing] = useState(null);
  const [saving, setSaving] = useState(false);
  const [formError, setFormError] = useState(null);

  const filters = { search: search || undefined, categorie: categorie || undefined };
  const { medicaments, loading, error, refetch, pagination } = useMedicaments(filters);
  const { categories } = useCategories();

  const handleCreate = () => {
    setEditing(null);
    setShowForm(true);
    setFormError(null);
  };

  const handleEdit = (m) => {
    setEditing(m);
    setShowForm(true);
    setFormError(null);
  };

  const handleSubmit = async (payload) => {
    setSaving(true);
    setFormError(null);
    try {
      if (editing) {
        await updateMedicament(editing.id, payload);
      } else {
        await createMedicament(payload);
      }
      setShowForm(false);
      setEditing(null);
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

  const handleDelete = async (id) => {
    if (!window.confirm('Désactiver ce médicament (soft delete) ?')) return;
    try {
      await deleteMedicament(id);
      refetch();
    } catch (err) {
      alert(err.response?.data?.detail || err.message);
    }
  };

  return (
    <div className="page medicaments-page">
      <header className="page-header">
        <h1>Médicaments</h1>
        <button type="button" className="btn-primary" onClick={handleCreate}>
          Ajouter un médicament
        </button>
      </header>

      <div className="filters">
        <input
          type="search"
          placeholder="Rechercher (nom, DCI)..."
          value={search}
          onChange={(e) => setSearch(e.target.value)}
        />
        <select value={categorie} onChange={(e) => setCategorie(e.target.value)}>
          <option value="">Toutes les catégories</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>{c.nom}</option>
          ))}
        </select>
      </div>

      {loading && <LoadingSpinner />}
      {error && <ErrorMessage message={error} onRetry={refetch} />}

      {!loading && !error && (
        <>
          <p className="count">{(pagination?.count ?? medicaments.length) > 0 ? `${pagination?.count ?? medicaments.length} médicament(s)` : 'Aucun médicament.'}</p>
          <div className="table-wrap">
            <table className="data-table">
              <thead>
                <tr>
                  <th>Nom</th>
                  <th>DCI</th>
                  <th>Catégorie</th>
                  <th>Forme / Dosage</th>
                  <th>Prix vente</th>
                  <th>Stock</th>
                  <th>Alerte</th>
                  <th>Actions</th>
                </tr>
              </thead>
              <tbody>
                {medicaments.map((m) => (
                  <tr key={m.id}>
                    <td>{m.nom}</td>
                    <td>{m.dci || '—'}</td>
                    <td>{categories.find((c) => c.id === m.categorie)?.nom ?? (m.categorie_nom || '—')}</td>
                    <td>{m.forme} / {m.dosage}</td>
                    <td>{Number(m.prix_vente).toFixed(2)}</td>
                    <td>{m.stock_actuel}</td>
                    <td>
                      {m.est_en_alerte ? (
                        <span className="badge badge-warning">Stock bas</span>
                      ) : (
                        '—'
                      )}
                    </td>
                    <td>
                      <button type="button" className="btn-sm" onClick={() => handleEdit(m)}>Modifier</button>
                      <button type="button" className="btn-sm btn-danger" onClick={() => handleDelete(m.id)}>Suppr.</button>
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
          <div className="modal" onClick={(e) => e.stopPropagation()}>
            <h2>{editing ? 'Modifier le médicament' : 'Nouveau médicament'}</h2>
            {formError && <ErrorMessage message={formError} />}
            <MedicamentForm
              medicament={editing}
              categories={categories}
              onSubmit={handleSubmit}
              onCancel={() => { setShowForm(false); setEditing(null); }}
              saving={saving}
            />
          </div>
        </div>
      )}
    </div>
  );
}
