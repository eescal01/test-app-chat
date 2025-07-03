// App.jsx
import { useAuth } from "react-oidc-context";

export default function App() {
  const auth = useAuth();

  if (auth.isLoading) return <p>Loading...</p>;
  if (auth.error) return <p>Oops... {auth.error.message}</p>;

  if (!auth.isAuthenticated) {
    return (
      <div>
        <h1>Welcome to the 1-1 Chat App</h1>
        <button onClick={() => auth.signinRedirect()}>Sign in with Google</button>
      </div>
    );
  }

  const signOutRedirect = () => {
    const clientId = "758g0k3knce0c6kp66goo5hgvk";
    const logoutUri = "http://localhost:5173/";
    const cognitoDomain = "https://google-auth-domain-dev.auth.us-east-1.amazoncognito.com";
    localStorage.clear();
    window.location.href = `${cognitoDomain}/logout?client_id=${clientId}&logout_uri=${encodeURIComponent(logoutUri)}`;
  };

  return (
    <div>
      <h2>👋 Hello, {auth.user?.profile?.email}</h2>
      <button onClick={signOutRedirect}>Sign Out</button>
    </div>
  );
}
