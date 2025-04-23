// src/utils/auth.js
export const setToken = (token) => {
  localStorage.setItem('et_auth_token', token);
};

export const getToken = () => {
  return localStorage.getItem('et_auth_token');
};

export const removeToken = () => {
  localStorage.removeItem('et_auth_token');
};
