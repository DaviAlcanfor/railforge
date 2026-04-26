import styles from '../styles/ModelEditor.module.css'

type ModelEditorProps = {
    value: string
    onChange: (value: string) => void
}

export default function ModelEditor(props: ModelEditorProps){
    return (
        <textarea
            className={styles.textarea}
            value={props.value}
            onChange={e => props.onChange(e.target.value)}
            placeholder='{ "project_name": "my-api", "models": [] }'
        />
    )
}