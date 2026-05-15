import { useEffect } from "react";
import Button from "../ui/Button"

type HomeSelectorProps = {
  selected: string;
  selectionOptions: string[];
  setSelected: (value: string) => void;
};


export default function HomeSelector({ selected, selectionOptions, setSelected }: HomeSelectorProps ) {


    useEffect(() => {
        console.log('selsection changed:', selected);
    }, [selected]); // runs whenever active changes

  return (
    <div style={{ height: "100%", display: "flex", flexDirection: "column", }}>
        {selectionOptions.map(selectionOption => (
            <Button key={selectionOption} text={selectionOption} onClick={() => setSelected(selectionOption)} additionalClasses={selected === selectionOption ? "selected" : ''}></Button>
        ))}
    </div>
  );
}
