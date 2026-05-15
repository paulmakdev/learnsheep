import { useEffect, useRef, type RefObject } from "react";

type ExcludeRect = { x: number; y: number; w: number; h: number };

type Props = {
  images: string[];
  count?: number;
  excludeRef?: RefObject<HTMLElement | null>;
  excludePadding?: number;
};

export default function ProceduralCollage({
  images,
  count = 60,
  excludeRef,
  excludePadding = 2,
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    let built = false;
    const container = containerRef.current;
    if (!container) return;

    const raf = requestAnimationFrame(() => {
      if (built) return;
      built = true;

      container.innerHTML = "";

      const excludes: ExcludeRect[] = [];

      if (excludeRef?.current) {
        const r = excludeRef.current.getBoundingClientRect();
        excludes.push({
          x: (r.left / window.innerWidth) * 100 - excludePadding,
          y: (r.top / window.innerHeight) * 100 - excludePadding,
          w: (r.width / window.innerWidth) * 100 + excludePadding * 2,
          h: (r.height / window.innerHeight) * 100 + excludePadding * 2,
        });
      }

      const overlaps = (x: number, y: number) =>
        excludes.some(
          (r) => x > r.x && x < r.x + r.w && y > r.y && y < r.y + r.h
        );

      for (let i = 0; i < count; i++) {
        const img = document.createElement("img");
        img.src = images[Math.floor(Math.random() * images.length)];

        let x!: number, y!: number;
        let attempts = 0;
        do {
          x = Math.random() * 120 - 10;
          y = Math.random() * 120 - 10;
        } while (overlaps(x, y) && ++attempts < 100);

        const size = 2 + Math.random();
        const rot = Math.random() * 360;
        const opacity = 0.15 + Math.random() * 0.25;

        img.style.position = "absolute";
        img.style.left = `${x}vw`;
        img.style.top = `${y}vh`;
        img.style.width = `${size}vw`;
        img.style.opacity = String(opacity);
        img.style.transform = `translate(-50%, -50%) rotate(${rot}deg)`;
        img.style.objectFit = "contain";
        img.style.filter = "grayscale(1) contrast(1.1)";
        img.style.mixBlendMode = "multiply";
        img.style.pointerEvents = "none";

        container.appendChild(img);
      }
    });

    return () => {
      built = true; // prevent the raf callback from running after unmount
      cancelAnimationFrame(raf);
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  return <div className="collage-container" ref={containerRef} />;
}
