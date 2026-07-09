import { NavLink } from "react-router-dom";

export default function Navbar() {
  return (
    <nav className="navbar">
      <NavLink to="/" end className="brand">
        <img src="/logorag.png" alt="viaRAG" className="brand-logo" />
      </NavLink>

      <div className="nav-links">
        <NavLink to="/" end className={({ isActive }) => (isActive ? "active" : "")}>
          Home
        </NavLink>
        <NavLink to="/predictor" className={({ isActive }) => (isActive ? "active" : "")}>
          Classificador
        </NavLink>
        <NavLink to="/knowledge" className={({ isActive }) => (isActive ? "active" : "")}>
          Conhecimento
        </NavLink>
        <NavLink to="/about" className={({ isActive }) => (isActive ? "active" : "")}>
          Sobre
        </NavLink>
      </div>
    </nav>
  );
}