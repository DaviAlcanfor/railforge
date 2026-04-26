import type { FrameworkType } from "../types/enums";
import type { Framework } from "../types/interfaces";


type FrameworkSelectorProps = {
    frameworks: Framework[]
    selected: FrameworkType 
    onChange: (value: FrameworkType) => void
}

export default function FrameworkSelector(props: FrameworkSelectorProps){
    return <>
        <label htmlFor="">
            <select 
                name="FrameworkSelector" 
                id="FrameworkSelector" 
                value={props.selected}
                onChange={
                    e => props.onChange(e.target.value as FrameworkType)
                }
            >
                {props.frameworks.map(f => (
                    <option key={f.name} value={f.name}>
                        {f.name}
                    </option>
                ))}
            </select>
        </label>
    </>
}