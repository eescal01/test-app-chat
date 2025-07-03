// src/Callback.jsx
import { useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import { COGNITO_DOMAIN, CLIENT_ID, REDIRECT_URI } from './config';

function Callback() {
  const navigate = useNavigate();
  const { search } = useLocation();

  useEffect(() => {
    const params = new URLSearchParams(search);
    const code = params.get('code');

    if (!code) {
      // Manejar error
      return;
    }

    const fetchTokens = async () => {
      const body = new URLSearchParams({
        grant_type: 'authorization_code',
        client_id: CLIENT_ID,
        code,
        redirect_uri: REDIRECT_URI,
      });

      try {
        const response = await fetch(`${COGNITO_DOMAIN}/oauth2/token`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body,
        });

        if (!response.ok) throw new Error('Token exchange failed');
        const data = await response.json();

        localStorage.setItem('id_token', data.id_token);
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);

        navigate('/chat');
      } catch (err) {
        alert('Error al intercambiar el código por tokens');
      }
    };

    fetchTokens();
  }, [search, navigate]);

  return <div>Procesando inicio de sesión...</div>;
}

export default Callback;