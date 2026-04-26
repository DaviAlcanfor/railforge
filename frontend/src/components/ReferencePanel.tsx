import styles from '../styles/ReferencePanel.module.css'
import { FieldType, GeneratesType } from "../types/enums"

type ReferencePanelProps = {
    acceptedTypes: FieldType[]
    generates: GeneratesType[]
}

export default function ReferencePanel(props: ReferencePanelProps){
    console.log(props.generates)
    return (
        <div className={styles.section}>
            <div className={styles.group}>
                <p className={styles.title}>Accepted Types</p>
                <ul className={styles.list}>
                    {props.acceptedTypes.map(t => (
                        <li key={t}>{t}</li>
                    ))}
                </ul>
            </div>

            <div className={styles.group}>
                <p className={styles.title}>Framework Generates</p>
                <ul className={styles.list}>
                    {props.generates.map(g => (
                        <li key={g}>{g}</li>
                    ))}
                </ul>
            </div>
        </div>
    )
}