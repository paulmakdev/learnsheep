type DefinitionProps = {
    topic: string,
    definition: string
    background_color?: string
}

export default function Definition({topic =  "", background_color = "var(--light)", definition = ""}: DefinitionProps) {
  return (
        <div style={{display: "flex", boxShadow: "var(--light-shadow-card-bottom)", flexDirection: "column", alignItems: "center", textAlign: "left", maxHeight: "20vh", width: "30vw", padding: "var(--standard-padding)", backgroundColor: background_color, borderRadius: "var(--mini-padding)"}}>
            <div className="emboldened">
                {topic}
            </div>
            <div>
                {definition}
            </div>
        </div>
  );
}
