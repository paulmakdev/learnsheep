type ModuleMiniCardProps = {
  background_color?: string,
  image_ref?: string,
  name: string
};

export default function ModuleMiniCardProps({
  background_color,
  image_ref,
  name
}: ModuleMiniCardProps) {
  return (
    <div style={{borderRadius: "var(--mini-padding)", breakInside: "avoid", fontSize: "var(--standard-font-size)", height: "100%", aspectRatio: "1"}}>
        <div style={{
            borderRadius: "var(--mini-padding)",
            backgroundColor: background_color ?? "var(--light)",
            padding: "var(--standard-padding)",
            display: "flex",
            flexDirection: "column",
            fontSize: "var(--standard-font-size)",
            height: "100%",
            maxHeight: "16vh",
            maxWidth: "16vh",
            boxShadow: "0 1px 2px rgba(0, 0, 0, 0.08), 0 8px 24px rgba(0, 0, 0, 0.12)",
            }}
        >
            <img src={image_ref} alt={name + " icon"} style={{imageRendering: "pixelated", maxHeight: "50%", objectFit: "contain", objectPosition: "center"}}/>
            <p className="emboldened" style={{marginTop: "var(--standard-padding)", marginBottom: "var(--standard-padding)", textAlign: "center"}}>{name}</p>
        </div>
    </div>
  )
}
