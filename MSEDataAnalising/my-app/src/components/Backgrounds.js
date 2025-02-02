import React, { useEffect, useState } from 'react';
import './Background.css';
import video1 from '../images/bck_video.mp4';
import image1 from '../images/finance_1.jpg';
import image2 from '../images/finance.jpg';
import image3 from '../images/visualise.jpg';

const Background = ({ playStatus, heroCount }) => {
    const [isVideoReady, setIsVideoReady] = useState(false);
    const [showVideo, setShowVideo] = useState(false); // Controls when to show the video
    const [currentImage, setCurrentImage] = useState(null);

    useEffect(() => {
        // Preload the images
        const images = [image1, image2, image3];
        images.forEach((src) => {
            const img = new Image();
            img.src = src;
        });

        // Preload the video
        const video = document.createElement('video');
        video.src = video1;
        video.oncanplaythrough = () => setIsVideoReady(true);
        video.load();
    }, []);

    useEffect(() => {
        // Update current image based on heroCount
        if (!playStatus) {
            if (heroCount === 0) setCurrentImage(image1);
            if (heroCount === 1) setCurrentImage(image2);
            if (heroCount === 2) setCurrentImage(image3);
        } else {
            if (isVideoReady) {
                setTimeout(() => setShowVideo(true), 100); // Wait 100ms
            }
        }
    }, [playStatus, heroCount, isVideoReady]);

    if (playStatus && showVideo) {
        return (
            <video className="background" autoPlay loop muted>
                <source src={video1} type="video/mp4" />
            </video>
        );
    } else {
        return (
            <div className="background-placeholder">
                <img
                    src={currentImage || image1}
                    className="background"
                    alt="Background Placeholder"
                />
            </div>
        );
    }
};

export default Background;