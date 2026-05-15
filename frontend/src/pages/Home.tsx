import Footer from '../components/layout/Footer';
import Title from '../components/home/Title';
import Login from '../components/home/Login';
import HomeSelector from '../components/home/HomeSelector.tsx'
import About from '../components/home/About'
import Unknown from './Unknown'
import { gsap } from "gsap";
import { Flip } from "gsap/Flip";
import { useEffect, useState, useRef } from 'react';
import StandardHeader from '../components/ui/StandardHeader.tsx';
import ProceduralCollage from '../components/home/CollageBackgroundMoving.tsx';
import LessonFinder from '../components/home/LessonFinder.tsx';
import LearnsheepGraySprite from "/learnsheep_sheep_sprite_gray.png"

gsap.registerPlugin(Flip);

export default function Home() {
    const selectionOptions = ["About Learnsheep", "Lesson Finder", "Login"]

    const [selected, setSelected] = useState("About Learnsheep")
    const [rendered, setRendered] = useState("About Learnsheep");

    const [titleVisible, setTitleVisible] = useState(true);

    const selectedComponentMap = {
        "Lesson Finder": () => <LessonFinder />,
        "Login": () => <Login />,
        "About Learnsheep": () => <About />,
    } as const;

    const SelectedComponent = selectedComponentMap[rendered as keyof typeof selectedComponentMap] ?? Unknown;

    useEffect(() => {
        if (selected != "About Learnsheep") {
               gsap.set('#title-id', { transformOrigin: 'top left' });
                gsap.to('#title-id', {
                    opacity: 1,
                    scale: 0.3,
                    height: "7.5vh",
                    marginBottom: 0,
                    duration: 0.3,
                    onComplete: () => {
                        setTitleVisible(false)
                    },
                })
                gsap.to('#main-content', {
                    opacity: 0,
                    duration: 0.3,
                    onComplete: () => setRendered(selected)
                });
        } else {
            setTitleVisible(true)
        }
        if (rendered != selected) {
            gsap.to('#main-content', {
                opacity: 0,
                duration: 0.15,
                onComplete: () => setRendered(selected)
            });
        }
    }, [selected])

    useEffect(() => {
    if (titleVisible) {
            requestAnimationFrame(() => {
                gsap.to('#title-id', {
                    opacity: 1,
                    height: 'auto',
                    scale: 1,
                    duration: 0.15,
                    marginBottom: "var(--largest-padding)",
                });
            });
        }
    }, [titleVisible]);

    useEffect(() => {
        requestAnimationFrame(() => {
            gsap.to('#main-content', { opacity: 1, duration: 0.15 });
        });
    }, [rendered]);

    const titleRef = useRef<HTMLDivElement>(null);

    return (
        <>
            <ProceduralCollage
            images={["/learnsheep_sheep.png"]}
            count={60}
            excludeRef={titleRef}
            animation={{
                sprite: {
                src: LearnsheepGraySprite,
                framesPerRow: 7,
                rows: 2,
                frameWidth: 21,   // width of one frame in pixels
                frameHeight: 17,  // height of one row in pixels
                },
                idleTimeout: 5,        // seconds before triggering
                activeFraction: 0.1,    // 10% of images animate
                spriteDisplaySize: 4,   // rendered size in vw
                fps: 12,                // sprite playback speed
                runDistance: 25,        // how far runners travel in vw
                jumpHeight: 7,         // how high jumpers arc in vh
                runDuration: 3,         // seconds for one run pass
                jumpDuration: 1,      // seconds for one jump cycle
            }}
            />
            <div id="basic-background" style={{height: "100dvh", maxHeight: "100dvh"}}>
                <StandardHeader></StandardHeader>
                <div ref={titleRef} style={{display: "flex", flexDirection: "column", height: "100%"}}>
                    <main>
                        {/*{titleVisible &&*/}
                        <div  id="title-id" style={{marginBottom: "var(--largest-padding)"}}>
                            <Title />
                        </div>
                        <div style={{display: "flex"}}>
                            <div style={{minWidth: "15vw"}}>
                                <HomeSelector selected={selected} selectionOptions={selectionOptions} setSelected={setSelected}/>
                            </div>

                            <div id="main-content" style={{"width": "100%", marginLeft: "var(--largest-padding)", "height": "67vh"}}>
                                <SelectedComponent />
                            </div>
                        </div>

                    </main>
                    {/* This box grows so that the footer is always on the bottom*/}
                    <div style={{flex: "1 1 0"}}>

                    </div>
                    <div style={{alignSelf: "end", fontSize: "var(--standard-font-size"}}>
                        <Footer />
                    </div>
                </div>
            </div>
        </>
    );
}
