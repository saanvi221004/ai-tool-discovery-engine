import React from 'react';
import { Link } from 'react-router-dom';
import './Navbar.css';

const Navbar = () => {
  return (
    <nav className="navbar">
      <div className="container">
        <Link to="/" className="navbar-brand">
          🤖 AI Tool Discovery
        </Link>
        <div className="navbar-nav">
          <Link to="/" className="nav-link">Home</Link>
          <Link to="/onboarding" className="nav-link">Find Tools</Link>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;
