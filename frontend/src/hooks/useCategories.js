import { useState, useEffect } from 'react';
import { fetchCategories } from '../api/categoriesApi';

/**
 * Hook pour la liste des catégories.
 * @returns {{ categories: Array, loading: boolean, error: string|null, refetch: function }}
 */
export const useCategories = () => {
  const [categories, setCategories] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(null);

  const load = async () => {
    setLoading(true);
    setError(null);
    try {
      const data = await fetchCategories();
      const list = data.results ?? (Array.isArray(data) ? data : []);
      setCategories(list);
    } catch (err) {
      setError(err.response?.data?.detail || err.message || 'Erreur lors du chargement');
      setCategories([]);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    load();
  }, []);

  return { categories, loading, error, refetch: load };
};
