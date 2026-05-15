type LessonCardProps = {
  title: string,
  link: string,
  description?: string,
  top_color?: string,
  top_text_color?: string,
  bottom_color?: string,
  bottom_text_color?: string
};

export default function ModuleMiniCardProps({
  title,
  top_color,
  top_text_color,
  bottom_color,
  bottom_text_color,
  description,
  link
}: LessonCardProps) {
  return (
      <a href={link} className="box-shadow hover-glow-scale" style={{display: "flex", textAlign: "left", borderRadius: "var(--mini-padding)", flexDirection: "column", flex: "1 1 0", textDecoration: "none", color: "inherit", marginBottom: "var(--standard-padding)"}}>
        <div style={{

            borderRadius: "var(--mini-padding) var(--mini-padding) 0 0",
            backgroundColor: top_color ?? "var(--card-top-bg)",
            color: top_text_color ?? "var(--standard-text-color)",
            padding: "var(--standard-padding)"
            }}
            className= "emboldened"
        >
          {title}
        </div>
        <div style={{
            borderRadius: "0 0 var(--mini-padding) var(--mini-padding)",
            backgroundColor: bottom_color ?? "var(--light)",
            color: bottom_text_color ?? "var(--standard-text-color)",
            padding: "var(--standard-padding)",
            whiteSpace: "pre-line",
            border: "1vh solid var(--card-bg)",
            borderWidth: "0 1px 1px 1px"
            }}
        >
            <p style={{margin: "0"}}>{description}</p>
        </div>
      </a>
  )
}
