import axiosInstance from './axiosConfig';

/**
 * Liste paginée des médicaments actifs.
 * @param {Object} params - search, categorie, page
 * @returns {Promise<Object>} Réponse paginée { count, results, next, previous }
 */
export const fetchMedicaments = async (params = {}) => {
  const response = await axiosInstance.get('/medicaments/', { params });
  return response.data;
};

/**
 * Détail d'un médicament.
 * @param {number} id
 * @returns {Promise<Object>}
 */
export const getMedicament = async (id) => {
  const response = await axiosInstance.get(`/medicaments/${id}/`);
  return response.data;
};

/**
 * Création d'un médicament.
 * @param {Object} data
 * @returns {Promise<Object>}
 */
export const createMedicament = async (data) => {
  const response = await axiosInstance.post('/medicaments/', data);
  return response.data;
};

/**
 * Mise à jour d'un médicament.
 * @param {number} id
 * @param {Object} data
 * @returns {Promise<Object>}
 */
export const updateMedicament = async (id, data) => {
  const response = await axiosInstance.patch(`/medicaments/${id}/`, data);
  return response.data;
};

/**
 * Soft delete d'un médicament.
 * @param {number} id
 */
export const deleteMedicament = async (id) => {
  await axiosInstance.delete(`/medicaments/${id}/`);
};

/**
 * Médicaments dont le stock est sous le seuil minimum.
 * @returns {Promise<Array>}
 */
export const fetchAlertes = async () => {
  const response = await axiosInstance.get('/medicaments/alertes/');
  return response.data;
};
