import { cloneElement, useState, useEffect, useRef } from 'react';
import ScrollIndicatorDown from './ScrollIndicatorDown';
import ScrollIndicatorUp from './ScrollIndicatorUp';

type ScrollerProps = {
  scale_factor: GLfloat;
  children: React.ReactElement[];
  updown?: boolean;
  changeScale?: boolean;
  scrollText?: string;
  setSelected: (value: number) => void;
};

export default function ScrollCounter({scale_factor = 1.5, children = [], setSelected, updown = false, changeScale = true, scrollText =  ""}: ScrollerProps) {
  const [count, setCount] = useState(0);

  const [changeUp, setChangeUp] = useState(false);
  const [changeDown, setChangeDown] = useState(false);

  const scrollContainerRef = useRef<HTMLDivElement>(null);
  const selectedRef = useRef<HTMLDivElement>(null);

  function safeChangeCount(change: number): void {
    setCount(prev => Math.max(Math.min(prev + change, children.length - 1), 0));
  }

  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    const handleWheel = (e: WheelEvent) => {
      e.preventDefault();
      setCount(prev => Math.max(Math.min(prev + (e.deltaY > 0 ? 1 : -1), children.length - 1), 0));

      {/* Used for giving the scroll indicators a little effect when scrolling */}
      if (e.deltaY > 0) {
        setChangeDown(true)
        const timeout = setTimeout(() => {
          setChangeDown(false);
        }, 100);

        return () => clearTimeout(timeout);
      } else {
        setChangeUp(true)
        const timeout = setTimeout(() => {
          setChangeUp(false);
        }, 100);

        return () => clearTimeout(timeout);
      }
    };

    container.addEventListener("wheel", handleWheel, { passive: false });
    return () => container.removeEventListener("wheel", handleWheel);
  }, [children.length]);

    useEffect(() => {
        setSelected(count)
    }, [count]);


    useEffect(() => {
        setCount(0);
    }, [children.length])


    useEffect(() => {
      const container = scrollContainerRef.current;
      const selected = selectedRef.current;
      if (!container || !selected) return;

      // Now TypeScript knows both are non-null
      const containerCenter = container.offsetWidth / 2;
      const selectedOffset = selected.offsetLeft;
      const selectedCenter = selected.offsetWidth / 2;

      container.scrollLeft = selectedOffset - containerCenter + selectedCenter;
    }, [count, children]);

    const [containerHeight, setContainerHeight] = useState(0);
    const [containerWidth, setContainerWidth] = useState(0);

  useEffect(() => {
    const container = scrollContainerRef.current;
    if (!container) return;

    const observer = new ResizeObserver(([entry]) => {
      setContainerHeight(entry.contentRect.height);
      setContainerWidth(entry.contentRect.width);
    });

    observer.observe(container);
    return () => observer.disconnect();
  }, []);

    const [itemHeight, setItemHeight] = useState(0);
    const [itemSpacing, setItemSpacing] = useState(0);

    useEffect(() => {
      if (!selectedRef.current) return;
      setItemHeight(selectedRef.current.offsetHeight);
    }, [count, containerHeight]);

    // itemSpacing = itemHeight + gap
    useEffect(() => {
      if (!scrollContainerRef.current) return;
      const gap = parseFloat(getComputedStyle(scrollContainerRef.current).gap) || 0;
      setItemSpacing(itemHeight + gap);
    }, [itemHeight]);



  return (
    <>
    <div style={{display: "flex", flexDirection: updown ? "column" : "row", height: "100%"}}>


    <div
      className="button hover-fade"
      style={{color: "var(--primary-text-color)", padding: "var(--mini-padding)"}}
      onClick={() => safeChangeCount(-1)}>
        <p style={{textAlign: "center", margin: "0", color: "inherit"}}>
          {scrollText} ↑
        </p>
    </div>
      <div
        ref={scrollContainerRef}
        style={{
          overflow: "hidden",
          height: "100%",
          width: "100%",
          position: "relative",
          display: "flex",
          alignItems: updown ? "none" : "center",
          justifyContent: "center",
          flex: "1 1 0",
          padding: "var(--standard-padding)"
        }}
      >
        <div
          style={{
            flexDirection: updown ? "column" : "row",
            alignItems: "center",
            gap: "var(--standard-padding)",
            transform: updown
              ? `translateY(${ containerHeight / 4- count * itemSpacing - itemHeight / 2}px)`
              : `translateX(${containerWidth / 4 - count * itemSpacing - itemHeight / 2}px)`,
            transition: "transform 250ms ease",
          }}
        >
          {children.map((child, i) => {
          const scale = changeScale ? (Math.abs(count - i) == 0 ? 1 : Math.abs(count - i) <= 1 ? (1+scale_factor)/2 : scale_factor ) : 1;           return (
              <div
                key={i}
                ref={i === count ? selectedRef : null}
                style={{
                  flexShrink: 0,
                  transform: `scale(${scale})`,
                  transition: "transform 250ms ease",
                  cursor: "pointer",
                }}
                onClick={() => setCount(i)}
              >
              {    cloneElement(child as React.ReactElement<any>, {
      background_color: count == i ? "var(--highlight)" : null,
    })}
              </div>
          );
          })}
        </div>
        <div style={{
            position: "absolute",
            bottom: "0",
            right: "0",
            transition: "transform 100ms ease",
            transform: changeDown ? "scale(1.3)" : "scale(1)",
            height: "var(--standard-padding)",
          }}
        >
          <ScrollIndicatorDown></ScrollIndicatorDown>
        </div>
        <div style={{
            position: "absolute",
            top: "0",
            right: "0",
            transition: "transform 100ms ease",
            transform: changeUp ? "scale(1.3)" : "scale(1)",
            height: "var(--standard-padding)",
          }}
        >
          <ScrollIndicatorUp></ScrollIndicatorUp>
        </div>
      </div>
    <div
      className="button hover-fade"
      style={{color: "var(--primary-text-color)", padding: "var(--mini-padding)"}}
      onClick={() => safeChangeCount(1)}>

        <p style={{textAlign: "center", margin: "0", color: "inherit"}}>
          {scrollText} ↓
        </p>
    </div>
        </div>
    </>
  );
}
