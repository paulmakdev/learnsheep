import InfoCard from "../ui/InfoCard"

export default function About() {
    const infoTextDict = {
        "What is Learnsheep?": "Learnsheep is an educational site created to give everyone access to high-quality, easy-to-understand education." ,
        "Who is Learnsheep for?": "Everyone! Don't understand something? Highlight it, and click \"rephrase\" or ask Woolie the Sheep (our backend) to explain more.",
        "Why is Learnsheep unique?": "Sometimes hard concepts are not explained in a way everyone can understand; Learnsheep is trying to fix that. \n\n Every lesson is crafted with common language and does not assume prior knowledge."
    }

  return (
    <div style={{ height: "100%", columns: "2", gap: "var(--standard-padding)"}}>
        {Object.entries(infoTextDict).map(([topText, bottomText]) => (
            <InfoCard key={topText} top_text={topText} bottom_text={bottomText}></InfoCard>
        ))}
    </div>
  );
}
