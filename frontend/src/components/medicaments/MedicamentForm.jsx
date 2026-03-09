import { useState, useEffect } from 'react';

/**
 * Formulaire création / édition d'un médicament.
 * Les appels API sont faits par le parent (page) qui passe onSubmit.
 */
export default function MedicamentForm({ medicament, categories, onSubmit, onCancel, saving }) {
  const [form, setForm] = useState({
    nom: '',
    dci: '',
    categorie: '',
    forme: '',
    dosage: '',
    prix_achat: '',
    prix_vente: '',
    stock_actuel: '',
    stock_minimum: '',
    date_expiration: '',
    ordonnance_requise: false,
  });

  useEffect(() => {
    if (medicament) {
      setForm({
        nom: medicament.nom ?? '',
        dci: medicament.dci ?? '',
        categorie: medicament.categorie ?? '',
        forme: medicament.forme ?? '',
        dosage: medicament.dosage ?? '',
        prix_achat: medicament.prix_achat ?? '',
        prix_vente: medicament.prix_vente ?? '',
        stock_actuel: medicament.stock_actuel ?? '',
        stock_minimum: medicament.stock_minimum ?? '',
        date_expiration: medicament.date_expiration ?? '',
        ordonnance_requise: medicament.ordonnance_requise ?? false,
      });
    }
  }, [medicament]);

  const handleChange = (e) => {
    const { name, value, type, checked } = e.target;
    setForm((prev) => ({
      ...prev,
      [name]: type === 'checkbox' ? checked : value,
    }));
  };

  const handleSubmit = (e) => {
    e.preventDefault();
    const payload = {
      ...form,
      categorie: form.categorie || null,
      prix_achat: form.prix_achat ? Number(form.prix_achat) : 0,
      prix_vente: form.prix_vente ? Number(form.prix_vente) : 0,
      stock_actuel: form.stock_actuel ? Number(form.stock_actuel) : 0,
      stock_minimum: form.stock_minimum ? Number(form.stock_minimum) : 0,
    };
    onSubmit(payload);
  };

  return (
    <form onSubmit={handleSubmit} className="medicament-form">
      <div className="form-row">
        <label>Nom commercial *</label>
        <input name="nom" value={form.nom} onChange={handleChange} required />
      </div>
      <div className="form-row">
        <label>DCI</label>
        <input name="dci" value={form.dci} onChange={handleChange} />
      </div>
      <div className="form-row">
        <label>Catégorie *</label>
        <select name="categorie" value={form.categorie} onChange={handleChange} required>
          <option value="">-- Choisir --</option>
          {categories.map((c) => (
            <option key={c.id} value={c.id}>{c.nom}</option>
          ))}
        </select>
      </div>
      <div className="form-row">
        <label>Forme galénique *</label>
        <input name="forme" value={form.forme} onChange={handleChange} required />
      </div>
      <div className="form-row">
        <label>Dosage *</label>
        <input name="dosage" value={form.dosage} onChange={handleChange} required />
      </div>
      <div className="form-row">
        <label>Prix d'achat *</label>
        <input type="number" step="0.01" min="0" name="prix_achat" value={form.prix_achat} onChange={handleChange} required />
      </div>
      <div className="form-row">
        <label>Prix de vente *</label>
        <input type="number" step="0.01" min="0" name="prix_vente" value={form.prix_vente} onChange={handleChange} required />
      </div>
      <div className="form-row">
        <label>Stock actuel</label>
        <input type="number" min="0" name="stock_actuel" value={form.stock_actuel} onChange={handleChange} />
      </div>
      <div className="form-row">
        <label>Stock minimum</label>
        <input type="number" min="0" name="stock_minimum" value={form.stock_minimum} onChange={handleChange} />
      </div>
      <div className="form-row">
        <label>Date d'expiration *</label>
        <input type="date" name="date_expiration" value={form.date_expiration} onChange={handleChange} required />
      </div>
      <div className="form-row checkbox">
        <label>
          <input type="checkbox" name="ordonnance_requise" checked={form.ordonnance_requise} onChange={handleChange} />
          Ordonnance requise
        </label>
      </div>
      <div className="form-actions">
        <button type="button" onClick={onCancel}>Annuler</button>
        <button type="submit" disabled={saving}>{saving ? 'Enregistrement...' : 'Enregistrer'}</button>
      </div>
    </form>
  );
}
