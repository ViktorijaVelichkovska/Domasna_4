import React, { useState, useEffect } from 'react';
//import './Hero.css';
//import arrow_btn from '../../images/button.png';
//import play_icon from '../../images/play-btn.png';
//import pause_icon from '../../images/stop-btn.png';
import { NavLink } from 'react-router-dom';
import { BsMouse } from 'react-icons/bs';
import { Link } from "react-scroll"; // Import Link from react-scroll


const Hero = ({ heroData, setHeroCount, heroCount, setPlayStatus, playStatus }) => {
    // Automatically change the hero count every 5 seconds
    useEffect(() => {
        const interval = setInterval(() => {
            setHeroCount((prevCount) => (prevCount + 1) % 3); // Loop back to 0 after 2
        }, 20000); // Change every 5 seconds

        return () => clearInterval(interval); // Clean up the interval on component unmount
    }, [setHeroCount]);

    return (
        <div className="hero">
            <div className="hero-text">
                <p>{heroData.text1}</p>
                <p>{heroData.text2}</p>
            </div>
            <div className="hero-explore">
                <p>Новости</p>
                <Link to="news" smooth={true} duration={500}>
                    <img src={arrow_btn} alt="Scroll to News" />
                </Link>
            </div>
            <div className="hero-dot-play">
                <ul className="hero-dots">
                    <li
                        onClick={() => setHeroCount(0)}
                        className={heroCount === 0 ? 'hero-dot orange' : 'hero-dot'}
                    ></li>
                    <li
                        onClick={() => setHeroCount(1)}
                        className={heroCount === 1 ? 'hero-dot orange' : 'hero-dot'}
                    ></li>
                    <li
                        onClick={() => setHeroCount(2)}
                        className={heroCount === 2 ? 'hero-dot orange' : 'hero-dot'}
                    ></li>
                </ul>
                <div className="hero-play">
                    <img
                        onClick={() => setPlayStatus(!playStatus)}
                        {/* eslint-disable-next-line no-undef */}
                        src={playStatus ? pause_icon : play_icon}
                        alt=""
                    />
                </div>
            </div>
            <div className="floating-icon">
                <a href="#feature">
                    <BsMouse color="#3c096c" size={25} className="mouse" />
                </a>
            </div>
        </div>
    );
};

export default Hero;