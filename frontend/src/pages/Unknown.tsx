import { useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import learnsheep_sheep_sad from "../assets/learnsheep_sheep_sad.png"


export default function Unknown() {
  const navigate = useNavigate();

  useEffect(() => {
    const timer = setTimeout(() => {
      navigate('/', { replace: true });
    }, 3000); // 3 seconds

    return () => clearTimeout(timer);
  }, [navigate]);

  return (
    <div style={{display: "flex", flexDirection: "column", alignItems: "center"}}>
      <h1>Page not found</h1>
        <div style={{height: "20vh", width: "20vh"}}>
          <img src={learnsheep_sheep_sad} alt="Learnsheep Sheep sad that no pages match the URL." style={{imageRendering: "pixelated", width: "100%", maxHeight: "100%", objectFit: "contain", objectPosition: "bottom"}}/>
        </div>
      <p>Redirecting you back home in 3 seconds...</p>
    </div>
  );
}
