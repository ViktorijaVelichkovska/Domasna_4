import './Navbar.css';
import { NavLink } from 'react-router-dom';
import logo from '../images/white-logo.png';
import React from 'react'



export default function Navbar() {
    return (
        <nav className="nav">
            <div className="logo">
                <ul id="logo">
                    <li>
                        <NavLink to="/">
                            <img src={logo} alt="logo" width="280" height="66"/>
                        </NavLink>
                    </li>
                </ul>
            </div>
            <div className="nav-links">
                <ul className="pages">
                    <li>
                        <NavLink
                            to="/about"
                            className={({isActive}) => (isActive ? 'active' : '')}
                        >
                            За Берзата
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to="/show-data"
                            className={({isActive}) => (isActive ? 'active' : '')}
                        >
                            Издавачи
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to="/visualisation"
                            className={({isActive}) => (isActive ? 'active' : '')}
                        >
                            Визуелизација
                        </NavLink>
                    </li>
                    <li>
                        <NavLink
                            to="/technical-analysis"
                            className={({isActive}) => (isActive ? 'active' : '')}
                        >
                            Техничка Анализа
                        </NavLink>
                    </li>
                </ul>
            </div>

        </nav>
    );
}