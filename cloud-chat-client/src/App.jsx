// src/App.jsx
import { COGNITO_DOMAIN, CLIENT_ID, REDIRECT_URI, RESPONSE_TYPE, SCOPE } from './config';

function App() {
  const handleLogin = () => {
    const url = `${COGNITO_DOMAIN}/oauth2/authorize?response_type=${RESPONSE_TYPE}&client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&scope=${SCOPE}`;
    window.location.href = url;
  };

  return (
    <div style={{ display: 'flex', flexDirection: 'column', alignItems: 'center', marginTop: 100 }}>
      <h1>Iniciar sesión</h1>
      <button onClick={handleLogin} style={{ padding: '10px 20px', fontSize: 18 }}>
        Sign in with Google
      </button>
    </div>
  );
}

export default App;