import React from "react";
import Header from "./components/header";
import MainContent from "./components/mainContent";
import Footer from "./components/footer";

const COGNITO_DOMAIN = 'https://google-auth-domain-dev.auth.us-east-1.amazoncognito.com';
const CLIENT_ID = '758g0k3knce0c6kp66goo5hgvk';
const REDIRECT_URI = 'https://main.d2p1llmpk1i4a9.amplifyapp.com/callback';


export default function App() {
  const login = () => {
    const url = `${COGNITO_DOMAIN}/login?response_type=code&client_id=${CLIENT_ID}&redirect_uri=${encodeURIComponent(REDIRECT_URI)}&scope=openid+email+profile`;
    window.location.href = url;
  };

  // return (
  //   <div>
  //     <h1>Login</h1>
  //     <button onClick={login}>Sign in with Google</button>
  //   </div>
  // );
  return (
    <div className="relative flex size-full min-h-screen flex-col bg-gray-50 group/design-root overflow-x-hidden" style={{ fontFamily: '"Plus Jakarta Sans", "Noto Sans", sans-serif' }}>
      <div className="layout-container flex h-full grow flex-col">
        <Header />
        <MainContent />
        <Footer />
      </div>
    </div>
  );

}
