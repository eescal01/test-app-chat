import React from "react";
import './Login.css';
import assets from "../../assets/assets";

const style = {
    minHeight: "100vh",
    minWidth: "100vw",
    background: `url(${assets.background}) no-repeat center center fixed`,
    backgroundSize: "cover",
    display: "flex",
    flexDirection: "column", // Mejor para apilar elementos verticalmente
    justifyContent: "center",
    alignItems: "center",
    padding: "2rem", // Espacio interno para pantallas pequeñas
    boxSizing: "border-box"
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