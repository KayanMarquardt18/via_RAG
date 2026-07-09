import { useEffect, useRef } from "react";

/**
 * Campo de estrelas com paralaxe sutil baseado no movimento do mouse.
 * Usa canvas em vez de imagens/gifs para ser leve e nítido em qualquer resolução.
 */
export default function StarField() {
  const canvasRef = useRef(null);

  useEffect(() => {
    const canvas = canvasRef.current;
    const ctx = canvas.getContext("2d");

    const prefersReducedMotion = window.matchMedia(
      "(prefers-reduced-motion: reduce)"
    ).matches;

    let stars = [];
    let mouseX = 0;
    let mouseY = 0;
    let animationId;

    function resize() {
      canvas.width = window.innerWidth;
      canvas.height = window.innerHeight;
      generateStars();
    }

    function generateStars() {
      const count = Math.floor((canvas.width * canvas.height) / 9000);
      stars = Array.from({ length: count }, () => ({
        x: Math.random() * canvas.width,
        y: Math.random() * canvas.height,
        radius: Math.random() * 1.3 + 0.3,
        depth: Math.random() * 0.6 + 0.2, // estrelas "mais distantes" se movem menos
        twinkleSpeed: Math.random() * 0.015 + 0.005,
        twinklePhase: Math.random() * Math.PI * 2,
      }));
    }

    function draw() {
      ctx.clearRect(0, 0, canvas.width, canvas.height);

      const offsetX = prefersReducedMotion ? 0 : (mouseX - canvas.width / 2) * 0.01;
      const offsetY = prefersReducedMotion ? 0 : (mouseY - canvas.height / 2) * 0.01;

      for (const star of stars) {
        star.twinklePhase += star.twinkleSpeed;
        const twinkle = 0.55 + Math.sin(star.twinklePhase) * 0.45;

        const x = star.x + offsetX * star.depth;
        const y = star.y + offsetY * star.depth;

        ctx.beginPath();
        ctx.arc(x, y, star.radius, 0, Math.PI * 2);
        ctx.fillStyle = `rgba(232, 234, 240, ${twinkle})`;
        ctx.fill();
      }

      animationId = requestAnimationFrame(draw);
    }

    function handleMouseMove(e) {
      mouseX = e.clientX;
      mouseY = e.clientY;
    }

    resize();
    draw();

    window.addEventListener("resize", resize);
    if (!prefersReducedMotion) {
      window.addEventListener("mousemove", handleMouseMove);
    }

    return () => {
      cancelAnimationFrame(animationId);
      window.removeEventListener("resize", resize);
      window.removeEventListener("mousemove", handleMouseMove);
    };
  }, []);

  return (
    <div className="starfield">
      <canvas ref={canvasRef} />
    </div>
  );
}