import { useState, useEffect } from 'react';

/**
 * Formulaire de création d'une vente : lignes médicament + quantité.
 * Les médicaments disponibles sont passés en props (liste depuis l'API).
 */
export default function VenteForm({ medicaments, onSubmit, onCancel, saving }) {
  const [notes, setNotes] = useState('');
  const [lignes, setLignes] = useState([{ medicament: '', quantite: 1 }]);

  const addLigne = () => {
    setLignes((prev) => [...prev, { medicament: '', quantite: 1 }]);
  };

  const removeLigne = (index) => {
    if (lignes.length <= 1) return;
    setLignes((prev) => prev.filter((_, i) => i !== index));
  };

  const updateLigne = (index, field, value) => {
    setLignes((prev) => {
      const next = [...prev];
      next[index] = { ...next[index], [field]: field === 'quantite' ? Number(value) || 0 : value };
      return next;
    });
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const validLignes = lignes
      .filter((l) => l.medicament && l.quantite > 0)
      .map((l) => ({ medicament: Number(l.medicament), quantite: l.quantite }));
    if (validLignes.length === 0) {
      return;
    }
    onSubmit({ notes: notes || undefined, lignes: validLignes });
  };

  return (
    <form onSubmit={handleSubmit} className="vente-form">
      <div className="form-row">
        <label>Notes (optionnel)</label>
        <textarea
          name="notes"
          value={notes}
          onChange={(e) => setNotes(e.target.value)}
          rows={2}
          placeholder="Remarques sur la vente..."
        />
      </div>
      <div className="form-section">
        <div className="form-row head">
          <span>Médicament</span>
          <span>Quantité</span>
          <span className="col-action" />
        </div>
        {lignes.map((ligne, index) => (
          <div key={index} className="form-row ligne">
            <select
              value={ligne.medicament}
              onChange={(e) => updateLigne(index, 'medicament', e.target.value)}
              required
            >
              <option value="">-- Choisir --</option>
              {medicaments.map((m) => (
                <option key={m.id} value={m.id}>
                  {m.nom} ({m.dosage}) — Stock: {m.stock_actuel}
                </option>
              ))}
            </select>
            <input
              type="number"
              min="1"
              value={ligne.quantite}
              onChange={(e) => updateLigne(index, 'quantite', e.target.value)}
            />
            <button type="button" className="btn-sm" onClick={() => removeLigne(index)} disabled={lignes.length <= 1}>
              Retirer
            </button>
          </div>
        ))}
        <button type="button" className="btn-add-line" onClick={addLigne}>
          + Ajouter une ligne
        </button>
      </div>
      <div className="form-actions">
        <button type="button" onClick={onCancel}>Annuler</button>
        <button type="submit" disabled={saving}>
          {saving ? 'Enregistrement...' : 'Enregistrer la vente'}
        </button>
      </div>
    </form>
  );
}
