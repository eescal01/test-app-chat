import { COGNITO_DOMAIN, CLIENT_ID, REDIRECT_URI, RESPONSE_TYPE, SCOPE } from './config';

// Ahora puedes usar estas variables en tu componente App
export default function App() {
  const login = () => {
    const url = `${COGNITO_DOMAIN}/login?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&scope=openid+email+profile`;
    window.location.href = url;
  };

  return (
    <div>
      <h1>Login</h1>
      <button onClick={login}>Sign in with Google</button>
    </div>
  );
}
