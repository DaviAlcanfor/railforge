import styles from '../styles/FrameworkSelector.module.css'
import type { FrameworkType } from "../types/enums"
import type { Framework } from "../types/interfaces"

type FrameworkSelectorProps = {
    frameworks: Framework[]
    selected: FrameworkType
    onChange: (value: FrameworkType) => void
}

export default function FrameworkSelector(props: FrameworkSelectorProps){
    return (
        <div className={styles.selector}>
            {props.frameworks.map(f => (
                <label key={f.name} className={styles.option}>
                    <input
                        type="radio"
                        name="framework"
                        value={f.name}
                        checked={props.selected === f.name}
                        onChange={e => props.onChange(e.target.value as FrameworkType)}
                    />
                    <span>{f.name}</span>
                </label>
            ))}
        </div>
    )
}