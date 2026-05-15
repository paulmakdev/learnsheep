type InfoCardProps = {
  top_color?: string;
  bottom_color?: string;
  top_text_color?: string;
  bottom_text_color?: string;
  top_text: string;
  bottom_text: string;
};

export default function InfoCard({
  top_color,
  bottom_color,
  top_text_color,
  bottom_text_color,
  top_text,
  bottom_text
}: InfoCardProps) {
  return (
    <div style={{borderRadius: "var(--mini-padding)", breakInside: "avoid", fontSize: "var(--standard-font-size)", boxShadow: "var(--shadow-card)"}}>
        <div style={{
            borderRadius: "var(--mini-padding) var(--mini-padding) 0 0",
            backgroundColor: top_color ?? "var(--highlight)",
            color: top_text_color ?? "var(--standard-text-color)",
            padding: "var(--standard-padding)",
            }}
        >
            <p className = "emboldened" style={{margin: "0"}}>{top_text}</p>
        </div>
        <div style={{
            borderRadius: "0 0 var(--mini-padding) var(--mini-padding)",
            backgroundColor: bottom_color ?? "var(--light)",
            color: bottom_text_color ?? "var(--standard-text-color)",
            padding: "var(--standard-padding)",
            marginBottom: "var(--standard-padding)",
            whiteSpace: "pre-line",
            border: "1vh solid var(--card-bg)",
            borderWidth: "0 1px 1px 1px",
            }}
        >
            <p style={{margin: "0"}}>{bottom_text}</p>
        </div>
    </div>
  );
}
