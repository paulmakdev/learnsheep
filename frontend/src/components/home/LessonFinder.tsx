import { useState, useEffect } from "react";
import LessonExplorer from "./LessonExplorer"
import LessonSearcher from "./LessonSearcher"
import SmallButton from "../ui/SmallButton"

export default function LessonFinder() {
    const findLessonOptions = ["Lesson Explorer", "Lesson Searcher", "Lesson List"]

    const [selected, setSelected] = useState("Lesson Explorer")
    const [rendered, setRendered] = useState("Lesson Explorer");

    const findOptionsMap = {
        "Lesson Explorer": () => <LessonExplorer />,
        "Lesson Searcher": () => <LessonSearcher />,
        "Lesson List": () => <LessonSearcher />
    } as const;

    const SelectedComponent = findOptionsMap[rendered as keyof typeof findOptionsMap];

    useEffect(() => {
        setRendered(selected)
    }, [selected])


  return (
    <div style={{height: "100%", display: "flex", flexDirection: "column"}}>
        <div style={{display: "flex", gap: "var(--mini-padding)"}}>
            {findLessonOptions.map(selectionOption => (
                <SmallButton key={selectionOption} text={selectionOption} onClick={() => setSelected(selectionOption)} additionalClasses={selected === selectionOption ? "selected" : ''}></SmallButton>
            ))}
        </div>
        <SelectedComponent />
    </div>
  );
}
