import learnsheep_sheep from "/learnsheep_sheep.png"
import { useSelector } from "react-redux";
import { type RootState } from "../../app/store";

export default function Title() {
  const user = useSelector(
    (state: RootState) => state.user.currentUser
  );

  return (
    <section style={{ maxHeight: "25vh"}}>
        <div style={{display: "flex", height: "100%"}}>
            <div style={{width: "15vw", paddingTop: "var(--standard-padding)", paddingRight: "var(--largest-padding)", paddingBottom: "0", display: "flex", alignItems: "bottom"}}>
                <img src={learnsheep_sheep} alt="Learnsheep Sheep happily looking out at title." style={{imageRendering: "pixelated", width: "100%", maxHeight: "100%", objectFit: "contain", objectPosition: "bottom"}}/>
            </div>
            <div style={{display: "flex", color: "var(--dark)", flexDirection: "column", maxHeight: "100%", justifyContent: "end"}}>
                <p className="sub-title" style={{margin: "0", opacity: "0.5"}}>A new way to learn</p>
                <h1 style={{margin: "0"}} className="big-title">Learnsheep</h1>
                <p className="highlighted-sub-title sub-title" style={{marginBottom: "0", marginTop: "var(--mini-padding)"}}>
                    Learning is for everyone, even
                    <span
                        style={{
                            color: user?.displayName ? "var(--primary-text-color)" : "var(--deep-highlight)",
                        }}
                        >
                        { " " + (user?.displayName || "sheep")}
                    </span>.
                </p>
            </div>
        </div>
    </section>
  );
}
