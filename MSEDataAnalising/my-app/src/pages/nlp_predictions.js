import NLP from "../components/NLP"
import LatestNews from "../components/LatestNews"

export default function Nlp_predictions() {
    return (
        <div style={{display: 'flex', justifyContent: 'center', alignItems: 'center', flexDirection: 'column'}}>
            <h1>Predictions</h1>
            <NLP />
            <LatestNews />
        </div>

    )

}