import React from "react";
import './Login.css';
import assets from "../../assets/assets";

const style = {
    background: `url(${assets.background}) no-repeat`,
    backgroundSize: 'cover',
    height: '100vh',
    display: 'flex',
    justifyContent: 'center',
    justifyContent: 'space-evenly'
};

const Login = () => {
    return (
        <div className="login" style={style}>
            <img src={assets.logo_big} alt="logo" className="logo" />
            here we are
        </div>
    )
}

export default Login;