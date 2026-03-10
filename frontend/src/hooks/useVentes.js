import { useState, useEffect, useCallback } from 'react';
import { fetchVentes } from '../api/ventesApi';

/**
 * Hook pour la liste des ventes avec filtres date.
 * @param {Object} filters - { date_from, date_to }
 * @returns {{ ventes: Array, loading: boolean, error: string|null, refetch: function, pagination: Object }}
 */
export const useVentes = (filters = {}) => {
  const [ventes, setVentes] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);
  const [pagination, setPagination] = useState({ count: 0, next: null, previous: null });

  const load = useCallback(async (page = 1) => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchVentes({ ...filters, page });
      setVentes(data.results ?? []);
      setPagination({
        count: data.count ?? 0,
        next: data.next,
        previous: data.previous,
      });
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Erreur lors du chargement');
      setVentes([]);
    } finally {
      setLoading(false);
    }
  }, [filters.date_from, filters.date_to]);

  useEffect(() => {
    load(1);
  }, [load]);

  return { ventes, loading, error, refetch: () => load(1), pagination };
};
