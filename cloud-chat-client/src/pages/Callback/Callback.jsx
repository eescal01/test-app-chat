import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import { COGNITO_DOMAIN, CLIENT_ID, REDIRECT_URI } from '../../config';

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
        console.log(data)
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

  return (
    <div style={{ textAlign: 'center', marginTop: 100, fontFamily: 'Plus Jakarta Sans, Arial, sans-serif' }}>
      <p>Logging you in with Google...</p>
    </div>
  );
} 