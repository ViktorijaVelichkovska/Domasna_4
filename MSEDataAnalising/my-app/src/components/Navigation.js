import { Link } from 'react-router-dom';

function Navigation() {
    return (
        <nav>
            <ul>
                <li><Link to="/">Home</Link></li>
                <li><Link to="/about">About</Link></li>
                <li><Link to="/show-data">Show Data</Link></li>
                <li><Link to="/technical-analysis">Technical Analysis</Link></li>

            </ul>
        </nav>
    );
}

export default Navigation;

