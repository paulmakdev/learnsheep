import { useEffect, useRef, type RefObject } from "react";
import gsap from "gsap";

// ---------------------------------------------------------------------------
// Types
// ---------------------------------------------------------------------------

type ExcludeRect = { x: number; y: number; w: number; h: number };

type SpriteConfig = {
  /** Path to the sprite sheet image */
  src: string;
  /** Total number of frames per row */
  framesPerRow: number;
  /** Total number of rows (animation types) */
  rows: number;
  /** Width of a single frame in pixels */
  frameWidth: number;
  /** Height of a single frame in pixels (= spritesheet height / rows) */
  frameHeight: number;
};

type AnimationConfig = {
  sprite: SpriteConfig;
  /** How many seconds of inactivity before animations trigger */
  idleTimeout?: number;
  /** Fraction of images that become animated (0–1) */
  activeFraction?: number;
  /** How large the animated sprite appears on screen (in vw) */
  spriteDisplaySize?: number;
  /** Frames per second for sprite playback */
  fps?: number;
  /** How far runners travel horizontally (in vw) */
  runDistance?: number;
  /** How high jumpers arc (in vh) */
  jumpHeight?: number;
  /** Duration of one run cycle in seconds */
  runDuration?: number;
  /** Duration of one jump cycle in seconds */
  jumpDuration?: number;
};

type Props = {
  images: string[];
  count?: number;
  excludeRef?: RefObject<HTMLElement | null>;
  excludePadding?: number;
  animation?: AnimationConfig;
};

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------

/** Row indices into the sprite sheet */
const ANIM_ROW = {
  run: 0,
  jump: 1,
} as const;

type AnimType = keyof typeof ANIM_ROW;

interface ParticleState {
  el: HTMLImageElement;
  spriteEl: HTMLCanvasElement;
  originX: number;
  originY: number;
  animType: AnimType;
  frameInterval: ReturnType<typeof setInterval> | null;
  gsapTween: gsap.core.Tween | null;
}

// ---------------------------------------------------------------------------
// Component
// ---------------------------------------------------------------------------

export default function ProceduralCollage({
  images,
  count = 60,
  excludeRef,
  excludePadding = 2,
  animation,
}: Props) {
  const containerRef = useRef<HTMLDivElement>(null);
  const particlesRef = useRef<ParticleState[]>([]);
  const idleTimerRef = useRef<ReturnType<typeof setTimeout> | null>(null);
  const isIdleRef = useRef(false);

  // ── Build collage once on mount ──────────────────────────────────────────

  useEffect(() => {
    let built = false;
    const container = containerRef.current;
    if (!container) return;

    const raf = requestAnimationFrame(() => {
      if (built) return;
      built = true;

      container.innerHTML = "";
      particlesRef.current = [];

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
        // Wrapper div holds both the collage img and (later) the sprite canvas
        const wrapper = document.createElement("div");
        wrapper.style.position = "absolute";
        wrapper.style.pointerEvents = "none";

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

        wrapper.style.left = `${x}vw`;
        wrapper.style.top = `${y}vh`;
        wrapper.style.width = `${size}vw`;
        wrapper.style.transform = `translate(-50%, -50%) rotate(${rot}deg)`;

        img.style.width = "100%";
        img.style.opacity = String(opacity);
        img.style.objectFit = "contain";
        img.style.filter = "grayscale(1) contrast(1.1)";
        img.style.mixBlendMode = "multiply";
        img.style.display = "block";

        // Sprite canvas — hidden until animation triggers
        const canvas = document.createElement("canvas");
        canvas.style.display = "none";
        canvas.style.position = "absolute";
        canvas.style.top = "0";
        canvas.style.left = "0";

        wrapper.appendChild(img);
        wrapper.appendChild(canvas);
        container.appendChild(wrapper);

        // Randomly assign an animation type
        const animType: AnimType =
          Math.random() < 0.5 ? "run" : "jump";

        particlesRef.current.push({
          el: img,
          spriteEl: canvas,
          originX: x,
          originY: y,
          animType,
          frameInterval: null,
          gsapTween: null,
        });
      }
    });

    return () => {
      built = true;
      cancelAnimationFrame(raf);
    };
  }, []); // eslint-disable-line react-hooks/exhaustive-deps

  // ── Idle detection + animation trigger ──────────────────────────────────

  useEffect(() => {
    if (!animation) return;

    const {
      sprite,
      idleTimeout = 10,
      activeFraction = 0.1,
      spriteDisplaySize = 4,
      fps = 12,
      runDistance = 30,
      jumpHeight = 20,
      runDuration = 3,
      jumpDuration = 1.5,
    } = animation;

    const spriteImage = new Image();
    spriteImage.src = sprite.src;

    const startAnimations = () => {
      if (isIdleRef.current) return;
      isIdleRef.current = true;

      const particles = [...particlesRef.current];
      // Shuffle and take activeFraction
      for (let i = particles.length - 1; i > 0; i--) {
        const j = Math.floor(Math.random() * (i + 1));
        [particles[i], particles[j]] = [particles[j], particles[i]];
      }
      const active = particles.slice(
        0,
        Math.max(1, Math.floor(particles.length * activeFraction))
      );

      // Compute canvas display size in pixels
      const displayPx =
        (spriteDisplaySize / 100) * window.innerWidth;

      active.forEach((p) => {
        // Hide the collage image, show the sprite canvas
        p.el.style.display = "none";
        const canvas = p.spriteEl;
        canvas.width = sprite.frameWidth;
        canvas.height = sprite.frameHeight;
        canvas.style.display = "block";
        canvas.style.width = `${displayPx}px`;
        canvas.style.height = `${displayPx}px`;
        canvas.style.imageRendering = "pixelated";

        const ctx = canvas.getContext("2d")!;
        const row = ANIM_ROW[p.animType];
        let frame = 1; // skip idle frame 0 during animation

        // Sprite playback
        const drawFrame = (f: number) => {
          ctx.clearRect(0, 0, sprite.frameWidth, sprite.frameHeight);
          ctx.drawImage(
            spriteImage,
            f * sprite.frameWidth,
            row * sprite.frameHeight,
            sprite.frameWidth,
            sprite.frameHeight,
            0,
            0,
            sprite.frameWidth,
            sprite.frameHeight
          );
        };

        if (p.animType !== "jump") {
          drawFrame(frame);
          p.frameInterval = setInterval(() => {
            frame = frame >= sprite.framesPerRow - 1 ? 1 : frame + 1;
            drawFrame(frame);
          }, 1000 / fps);
        }


        // GSAP movement
        const wrapper = canvas.parentElement as HTMLElement;

if (p.animType === "run") {
  const rotMatch = wrapper.style.transform.match(/rotate\(([-\d.]+)deg\)/);
  const rotDeg = rotMatch ? parseFloat(rotMatch[1]) : 0;
  const rotRad = (rotDeg * Math.PI) / 180;

  // Local "right" is perpendicular to local "up"
  const dirX = Math.cos(rotRad);
  const dirY = Math.sin(rotRad);

  const direction = Math.random() < 0.5 ? 1 : -1;
  const targetX = p.originX + dirX * runDistance * direction;
  const targetY = p.originY + dirY * runDistance * direction;

  canvas.style.transform = direction < 0 ? "scaleX(-1)" : "scaleX(1)";

  p.gsapTween = gsap.to(wrapper, {
    left: `${targetX}vw`,
    top: `${targetY}vh`,
    duration: runDuration,
    ease: "none",
    repeat: -1,
    yoyo: true,
    onRepeat: () => {
      const current = canvas.style.transform;
      canvas.style.transform =
        current === "scaleX(-1)" ? "scaleX(1)" : "scaleX(-1)";
    },
  });
} else {
  const rotMatch = wrapper.style.transform.match(/rotate\(([-\d.]+)deg\)/);
  const rotDeg = rotMatch ? parseFloat(rotMatch[1]) : 0;
  const rotRad = (rotDeg * Math.PI) / 180;

  const peakX = p.originX + Math.sin(rotRad) * jumpHeight;
  const peakY = p.originY - Math.cos(rotRad) * jumpHeight;

  const groundFrameDuration = 120;
  const riseDuration = jumpDuration * 0.4 * 1000;
  const fallDuration = jumpDuration * 0.4 * 1000;
  const landDuration = 150;

  let jumpActive = true;
  let activeTimeouts: ReturnType<typeof setTimeout>[] = [];

  const schedule = (ms: number, fn: () => void) => {
    const t = setTimeout(() => {
      if (jumpActive) fn();
    }, ms);
    activeTimeouts.push(t);
  };

  const runJumpCycle = () => {
    if (!jumpActive) return;

    // Clear any leftover timeouts from previous cycle before scheduling new ones
    activeTimeouts.forEach(clearTimeout);
    activeTimeouts = [];

    gsap.killTweensOf(wrapper);

    let t = 0;

    schedule(t, () => drawFrame(0)); t += groundFrameDuration;
    schedule(t, () => drawFrame(1)); t += groundFrameDuration;
    schedule(t, () => drawFrame(2)); t += groundFrameDuration;
    schedule(t, () => drawFrame(3)); t += groundFrameDuration;

    schedule(t, () => {
      drawFrame(4);
      gsap.to(wrapper, {
        left: `${peakX}vw`,
        top: `${peakY}vh`,
        duration: riseDuration / 1000,
        ease: "power2.out",
      });
    });
    t += riseDuration;

    schedule(t, () => {
      drawFrame(5);
      gsap.to(wrapper, {
        left: `${p.originX}vw`,
        top: `${p.originY}vh`,
        duration: fallDuration / 1000,
        ease: "power2.in",
      });
    });
    t += fallDuration;

    schedule(t, () => drawFrame(6));
    t += landDuration;

    schedule(t, () => runJumpCycle());
  };

  (p as any)._stopJump = () => {
    jumpActive = false;
    activeTimeouts.forEach(clearTimeout);
    activeTimeouts = [];
    gsap.killTweensOf(wrapper);
  };

  runJumpCycle();
}
      });
    };

    const stopAnimations = () => {
      if (!isIdleRef.current) return;
      isIdleRef.current = false;

      particlesRef.current.forEach((p) => {
        (p as any)._stopJump?.(); // ← add this first

        if (p.frameInterval) {
          clearInterval(p.frameInterval);
          p.frameInterval = null;
        }

        if (p.gsapTween) {
          p.gsapTween.kill();
          p.gsapTween = null;
        }

        const wrapper = p.el.parentElement as HTMLElement;
        gsap.to(wrapper, {
          left: `${p.originX}vw`,
          top: `${p.originY}vh`,
          duration: 0.8,
          ease: "power2.out",
        });

        p.spriteEl.style.display = "none";
        p.el.style.display = "block";
      });
    };

    const resetTimer = () => {
      if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
      if (isIdleRef.current) stopAnimations();
      idleTimerRef.current = setTimeout(startAnimations, idleTimeout * 1000);
    };

    const events = ["mousemove", "keydown", "scroll", "pointerdown"] as const;
    events.forEach((e) => window.addEventListener(e, resetTimer));
    resetTimer(); // start the initial timer

    return () => {
      events.forEach((e) => window.removeEventListener(e, resetTimer));
      if (idleTimerRef.current) clearTimeout(idleTimerRef.current);
      stopAnimations();
    };
  }, [animation]); // eslint-disable-line react-hooks/exhaustive-deps

  return <div className="collage-container" ref={containerRef} />;
}
