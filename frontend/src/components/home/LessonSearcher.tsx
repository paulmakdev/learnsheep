import LessonCard from "../ui/LessonCard"
import { mapLessonMetadata } from "../../routing-data/mapLessonMetadata"
import Scroller from "../ui/Scroller"
import Fuse from "fuse.js";
import { useState, useMemo } from "react";

export default function LessonSearcher() {
    const [query, setQuery] = useState("");

    const lessonData = Object.entries(mapLessonMetadata).map(
    ([id, value]) => ({
        id,
        ...value,
    })
    );

    const fuse = useMemo(() => {
        return new Fuse(lessonData, {
        keys: ["title", "description", "tags"],
        threshold: 0.4,
        });
    }, []);

    const results = useMemo(() => {
    if (!query) return lessonData;

    return fuse.search(query).map(r => r.item);
    }, [query, fuse, lessonData]);

  return (
    <div style={{ height: "100%", display: "flex", gap: "var(--standard-padding)"}}>
        <div style={{ height: "100%", display: "flex", flexDirection: "row", flex: "1", gap: "var(--standard-padding)"}}>
            <div style={{display: "flex", flexDirection: "column", flex: "4", height: "100%", borderRadius: "var(--mini-padding)"}}>
                <div style={{height: "var(--standard-padding)"}}>

                </div>
                <input
                    value={query}
                    onChange={(e) => setQuery(e.target.value)}
                    placeholder="Search any topic..."
                    style={{padding: "var(--smaller-padding)"}}
                />
                <div style={{height: "var(--smaller-padding)"}}>

                </div>
                <Scroller scale_factor={1} changeScale={false} setSelected={() => {}} updown={true} children=

                    {results!.map(lessonObject => (
                        <LessonCard
                            title={lessonObject.title ?? "no title yet :)"}
                            description={lessonObject.description ?? "no description yet :)"}
                            link={"/lesson/"+lessonObject.id}
                        >

                        </LessonCard>
                    ))}
                />
            </div>
        </div>
    </div>
  );
}
