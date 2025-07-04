import { COGNITO_DOMAIN, CLIENT_ID, REDIRECT_URI } from '../config';

export function login() {
  const url = `${COGNITO_DOMAIN}/login?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&scope=openid+email+profile`;
  window.location.href = url;
}

export function logout() {
  localStorage.removeItem('id_token');
  localStorage.removeItem('access_token');
  localStorage.removeItem('refresh_token');
  window.location.href = '/';
}

export function isAuthenticated() {
  return !!localStorage.getItem('access_token');
}

export function getToken() {
  return localStorage.getItem('access_token');
}

export function getUserInfo() {
  const token = localStorage.getItem('id_token');
  if (!token) return null;
  
  try {
    const payload = JSON.parse(atob(token.split('.')[1]));
    return {
      email: payload.email,
      name: payload.name,
      picture: payload.picture
    };
  } catch (error) {
    console.error('Error parsing token:', error);
    return null;
  }
}