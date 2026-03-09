import { useState, useEffect, useCallback } from 'react';
import { fetchMedicaments } from '../api/medicamentsApi';

/**
 * Hook pour la liste des médicaments avec filtres et pagination.
 * @param {Object} filters - { search, categorie }
 * @returns {{ medicaments: Array, loading: boolean, error: string|null, refetch: function, pagination: Object }}
 */
export const useMedicaments = (filters = {}) => {
  const [medicaments, setMedicaments] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({ count: 0, next: null, previous: null });

  const load = useCallback(async (page = 1) => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchMedicaments({ ...filters, page });
      setMedicaments(data.results ?? []);
      setPagination({
        count: data.count ?? 0,
        next: data.next,
        previous: data.previous,
      });
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Erreur lors du chargement');
      setMedicaments([]);
    } finally {
      setLoading(false);
    }
  }, [filters.search, filters.categorie]);

  useEffect(() => {
    load(1);
  }, [load]);

  return { medicaments, loading, error, refetch: () => load(1), pagination, loadPage: load };
};
