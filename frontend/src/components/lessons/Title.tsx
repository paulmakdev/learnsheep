import learnsheep_sheep from "/learnsheep_sheep.png"

type LessonTitleProps = {
    title: string,
    sub_title: string,
    background_color?: string
}

export default function Title({title =  "", background_color = "transparent", sub_title = ""}: LessonTitleProps) {
  return (
        <div style={{display: "flex", flexDirection: "column", alignItems: "center", maxHeight: "20vh", backgroundColor: background_color, borderRadius: "var(--mini-padding) var(--mini-padding) 0 0"}}>
            <div style={{width: "5vh", paddingBottom: "0", display: "flex", alignItems: "bottom"}}>
                <img src={learnsheep_sheep} alt="Learnsheep Sheep happily looking out at lesson title." style={{imageRendering: "pixelated", width: "100%", maxHeight: "100%", objectFit: "contain", objectPosition: "bottom"}}/>
            </div>
            <div style={{display: "flex", flexDirection: "column", maxHeight: "100%", justifyContent: "end", textAlign: "center"}}>
                <h1 style={{margin: "0"}} className="smaller-title">{title}</h1>
                <p className="highlighted-sub-title sub-title" style={{margin: "0"}}>{sub_title}</p>
            </div>
        </div>
  );
}
