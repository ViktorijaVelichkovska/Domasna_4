import React from 'react'
import './Companies.css'
import alk from '../../images/alkaloid.png'
import tlk from '../../images/tlkm.png'
import kmb from '../../images/komercijalna.png'
import nlb from '../../images/nlb.png'
import sb from '../../images/sb.png'


const Companies = () => {
    return (
        <div id="company-container">
            <div className="cmp">
                <div className="company-text">
                    <h1>Берза користена од над <span>150+</span> издавачи</h1>
                </div>
                <div className="images">
                    <img className="img1" src={sb} alt="sb"/>
                    <img className="img2" src={kmb} alt="kmb"/>
                    <img className="img3" src={alk} alt="alkaloid"/>
                    <img className="img4" src={nlb} alt="nlb"/>
                    <img className="img5" src={tlk} alt="tlk"/>
                </div>
            </div>
        </div>
    )
}
export default Companies;