import { prepareLessonUrl } from '../hooks/prepareLessonUrl';
import { lessonMap } from '../hooks/getLessonMap';
import Title from "../components/lessons/Title"
import { mapLessonMetadata } from "../routing-data/mapLessonMetadata"
import Unknown from "./Unknown"
import Definition from '../components/lessons/Definition';

export default function LessonPage() {
  const { lessonSlug, canonicalUrl } = prepareLessonUrl();

  const Component = lessonMap[lessonSlug];

  if (lessonSlug == "not-found") {
    return(<Unknown />)
  }

  return (
    <>
    <div id="basic-background" style={{background: "var(--light)", position: "relative"}}>

      <div style={{backgroundColor: "var(--light)", borderRadius: "var(--mini-padding)"}}>
        <link rel="canonical" href={canonicalUrl} />
        <div style={{position: "relative", padding: "var(--standard-padding)", paddingTop: "var(--largest-padding)", display: "flex", flexDirection: "column", alignItems: "center"}}>
          <Title title={mapLessonMetadata[lessonSlug]!.full_title ?? mapLessonMetadata[lessonSlug]!.title ?? lessonSlug} sub_title={mapLessonMetadata[lessonSlug]!.sub_title ?? mapLessonMetadata[lessonSlug]!.description ?? ""}></Title>
          <div style={{marginTop: "var(--largest-padding)", display: "flex", alignItems: "end", position: "absolute", top: "0", left: "0"}}>
            <a href="/" className="button selected hover-fade" style={{textDecoration: "none", cursor: "pointer", color: "white", display: "inline-block", borderRadius: "var(--mini-padding)"}}>
                <p style={{margin: "0", color: "inherit", padding: "var(--smaller-padding)"}}>← Back to Home</p>
            </a>
          </div>
          {mapLessonMetadata[lessonSlug]!.definitions &&
              <div style={{display: "flex", flexDirection: "column", alignItems: "center", gap: "var(--mini-padding)", marginTop: "var(--larger-padding)"}}>
                <p className="emboldened sub-title" style={{margin: "0"}}>Definitions</p>
                {
                Object.entries(mapLessonMetadata[lessonSlug]!.definitions).map(([topic, definition]) => (
                  <Definition topic={topic} definition={definition}></Definition>
                ))}



              </div>
          }
          <div>
            <div className="button" style={{display: "inline-block", padding: "var(--smaller-padding)", marginTop: "var(--standard-padding)"}}>
              Jump to Lesson Quiz
            </div>
          </div>
        </div>
        <div style={{display: "flex", flexDirection: "column", alignItems: "center", marginTop: "var(--standard-padding)"}}>
          <p className="emboldened sub-title" style={{margin: "0", marginBottom: "var(--standard-padding)"}}>The Story</p>
          <div style={{padding: "var(--largest-padding)", paddingTop: "0", minWidth: "50vw", alignItems: "center"}}>
            {Component ? <Component /> : <p style={{display: "inline"}}>"This is the " + (mapLessonMetadata[lessonSlug]!.full_title ?? mapLessonMetadata[lessonSlug]!.title ?? lessonSlug)+" lesson. It will be completed shortly. Check back soon!"</p>}
          </div>
        </div>

      </div>
    </div>

    </>
  );
}
