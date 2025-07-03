// src/auth.js
import { COGNITO_DOMAIN, CLIENT_ID, REDIRECT_URI } from '../config';

export function login() {
  const url = `${COGNITO_DOMAIN}/login?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&scope=openid+email+profile`;
  window.location.href = url;
}