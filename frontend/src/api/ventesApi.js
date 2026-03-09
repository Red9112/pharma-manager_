import axiosInstance from './axiosConfig';

/**
 * Liste paginée des ventes.
 * @param {Object} params - date_from, date_to, page
 * @returns {Promise<Object>}
 */
export const fetchVentes = async (params = {}) => {
  const response = await axiosInstance.get('/ventes/', { params });
  return response.data;
};

/**
 * Détail d'une vente.
 * @param {number} id
 * @returns {Promise<Object>}
 */
export const getVente = async (id) => {
  const response = await axiosInstance.get(`/ventes/${id}/`);
  return response.data;
};

/**
 * Création d'une vente (avec lignes).
 * @param {Object} data - { notes?, lignes: [{ medicament, quantite }] }
 * @returns {Promise<Object>}
 */
export const createVente = async (data) => {
  const response = await axiosInstance.post('/ventes/', data);
  return response.data;
};

/**
 * Annuler une vente.
 * @param {number} id
 * @returns {Promise<Object>}
 */
export const annulerVente = async (id) => {
  const response = await axiosInstance.post(`/ventes/${id}/annuler/`);
  return response.data;
};
