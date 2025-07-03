// index.js
import React from "react";
import ReactDOM from "react-dom/client";
import App from "./App";
import { AuthProvider } from "react-oidc-context";

const cognitoAuthConfig = {
  authority: "https://google-auth-domain-dev.auth.us-east-1.amazoncognito.com", // Hosted UI domain
  client_id: "758g0k3knce0c6kp66goo5hgvk",
  redirect_uri: "http://localhost:5173/callback",
  response_type: "code",
  scope: "openid email profile",
};

const root = ReactDOM.createRoot(document.getElementById("root"));

root.render(
  <React.StrictMode>
    <AuthProvider {...cognitoAuthConfig}>
      <App />
    </AuthProvider>
  </React.StrictMode>
);
