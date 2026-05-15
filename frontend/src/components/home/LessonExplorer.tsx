import ModuleMiniCard from "../ui/ModuleMiniCard"
import SubjectMiniCard from "../ui/SubjectMiniCard"
import LessonCard from "../ui/LessonCard"
import { mapLesson } from "../../routing-data/mapLesson"
import { mapLessonMetadata } from "../../routing-data/mapLessonMetadata"
import { useState, useEffect } from "react";
import Scroller from "../ui/Scroller"

export default function LessonExplorer() {
    const moduleOptions = Object.values(mapLesson)

    const [selectedModuleIndex, setSelectedModuleIndex] = useState(0)
    const [selectedModule, setSelectedModule] = useState(moduleOptions[0])

    const [selectedSubjectIndex, setSelectedSubjectIndex] = useState(0)
    const [selectedSubject, setSelectedSubject] = useState(Object.values(selectedModule.subjects)[0])


    useEffect(() => {
        setSelectedSubject(Object.values(selectedModule.subjects)[selectedSubjectIndex])
    }, [selectedSubjectIndex])

    useEffect(() => {
        setSelectedModule(moduleOptions[selectedModuleIndex])
        setSelectedSubject(Object.values(moduleOptions[selectedModuleIndex].subjects)[0])
        setSelectedSubjectIndex(0)
    }, [selectedModuleIndex]); // runs whenever active changes

  return (
    <div style={{ height: "100%", display: "flex", gap: "var(--standard-padding)"}}>
        <div style={{ height: "100%", display: "flex", flexDirection: "row", flex: "1", gap: "var(--standard-padding)"}}>
            <div style={{width: "20vh", display: "flex", flexDirection: "column", borderRadius: "var(--mini-padding)", marginBottom: "var(--standard-padding)", height: "100%"}}>
                <div style={{height: "var(--standard-padding)"}}>

                </div>
                <Scroller scrollText={"Module"} scale_factor={0.75} setSelected={setSelectedModuleIndex} updown={true} children={moduleOptions.map((moduleOption) => (
                    <ModuleMiniCard name={moduleOption["label"]} image_ref={moduleOption["image"]}></ModuleMiniCard>
                ))}/>
            </div>
            <div style={{width: "20vh",display: "flex", flexDirection: "column", borderRadius: "var(--mini-padding)", marginBottom: "var(--standard-padding)", height: "100%"}}>
                <div style={{height: "var(--standard-padding)"}}>

                </div>
                <Scroller scrollText={"Subject"} scale_factor={0.75} setSelected={setSelectedSubjectIndex} updown={true} children={Object.values(selectedModule.subjects).map((subjectOption) => (
                    <SubjectMiniCard name={subjectOption["label"]}></SubjectMiniCard>
                ))}/>
            </div>
        </div>
            <div style={{display: "flex", flexDirection: "column", flex: "4", height: "100%", borderRadius: "var(--mini-padding)"}}>
                <div style={{height: "var(--standard-padding)"}}>

                </div>
                <Scroller scrollText={"Lesson"} scale_factor={1} changeScale={false} setSelected={() => {}} updown={true} children=

                    {selectedSubject!.lessons.map((lessonOption) => (
                        <LessonCard
                            title={(mapLessonMetadata[lessonOption] ?? {"title": lessonOption}).title}
                            description={(mapLessonMetadata[lessonOption] ?? {"description": ""}).description}
                            link={(selectedModule["label"]+"/"+selectedSubject["label"]+"/"+lessonOption).toLowerCase().replaceAll(" ","-")}
                        >

                        </LessonCard>
                    ))}
                />
            </div>
    </div>
  );
}
