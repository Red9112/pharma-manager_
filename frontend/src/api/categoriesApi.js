import axiosInstance from './axiosConfig';

/**
 * Liste des catégories.
 * @returns {Promise<Array>}
 */
export const fetchCategories = async () => {
  const response = await axiosInstance.get('/categories/');
  return response.data;
};
