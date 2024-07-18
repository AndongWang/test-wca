
// Assisted by WCA@IBM
// Latest GenAI contribution: ibm/granite-20b-code-instruct-v2
import React, { useEffect, useRef } from 'react';
import './App.css';

function App() {
  const videoRef = useRef(null);
  let lastPlayTime = 0;

  useEffect(() => {
    const video = videoRef.current;

    // Monitor events to ensure that users cannot manually drag the progress bar forward
    video.addEventListener('timeupdate', (event) => {
      if (event.target.currentTime > lastPlayTime + 1) {
        event.target.currentTime = lastPlayTime;
      } else {
        lastPlayTime = event.target.currentTime;
      }
    });

    // Use localStorage to record the user's video progress
    video.addEventListener('pause', (event) => {
      localStorage.setItem('lastPlayTime', event.target.currentTime);
    });

    // Set the video progress to the last recorded position on page load
    window.onload = () => {
      const lastPlayTime = localStorage.getItem('lastPlayTime');
      if (lastPlayTime) {
        video.currentTime = lastPlayTime;
      }
    };
  }, []);

  return (
    <div className="App">
      <video ref={videoRef} src="oceans.mp4" controls>
      <track
          kind="captions"
          src="captions.vtt"
          srcLang="en"
          label="English"
          default
        />
      </video>
    </div>
  );
}

export default App;
