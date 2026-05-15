type ButtonProps = {
  text: string;
  onClick?: () => void;
  additionalClasses: string
};

export default function SmallButton({
  text,
  onClick,
  additionalClasses
}: ButtonProps) {
  return (
    <button
      onClick={onClick}
      className = {"button " + (additionalClasses ?? '')}
      style={{
        padding: 'var(--smaller-padding)',
        borderRadius: "var(--mini-padding)",
        cursor: 'pointer',
        marginBottom: "var(--smaller-padding)",
        fontSize: "var(--standard-font-size)",
        textAlign: "left"
      }}
    >
      <p style={{color: "inherit", margin: "0"}}>{text}</p>
    </button>
  );
}
