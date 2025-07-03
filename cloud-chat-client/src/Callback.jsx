// src/Callback.jsx
import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';

const COGNITO_DOMAIN = 'https://google-auth-domain-dev.auth.us-east-1.amazoncognito.com';
const CLIENT_ID = '758g0k3knce0c6kp66goo5hgvk';
const REDIRECT_URI = 'https://main.d2p1llmpk1i4a9.amplifyapp.com/callback';

export default function Callback() {
  const navigate = useNavigate();

  useEffect(() => {
    const code = new URLSearchParams(window.location.search).get('code');

    if (!code) {
      console.error('No code found in callback URL.');
      return;
    }

    const fetchTokens = async () => {
      try {
        const body = new URLSearchParams({
          grant_type: 'authorization_code',
          client_id: CLIENT_ID,
          code,
          redirect_uri: REDIRECT_URI,
        });

        const response = await fetch(`${COGNITO_DOMAIN}/oauth2/token`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
          },
          body,
        });

        const data = await response.json();

        if (data.error) {
          console.error('Token exchange error:', data);
          return;
        }

        // Save tokens for later use
        localStorage.setItem('id_token', data.id_token);
        localStorage.setItem('access_token', data.access_token);
        localStorage.setItem('refresh_token', data.refresh_token);

        // Redirect to chat room
        navigate('/chat');
      } catch (err) {
        console.error('Token exchange failed:', err);
      }
    };

    fetchTokens();
  }, [navigate]);

  return <p>Logging you in with Google...</p>;
}
