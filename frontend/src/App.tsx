import styles from './styles/App.module.css'

import FrameworkSelector from './components/FrameworkSelector'
import ModelEditor from './components/ModelEditor'
import ReferencePanel from './components/ReferencePanel'

import { generateProject, getFramework, getFrameworks } from './services/api'
import { FrameworkType } from './types/enums'
import { useEffect, useState } from 'react'

import type { Framework } from './types/interfaces'


function App() {

  const [frameworks, setFrameworks] = useState<Framework[]>([])
  const [selected, setSelected] = useState<FrameworkType>(FrameworkType.Rails)
  const [json, setJson] = useState<string>("")
  const [frameworkDetail, setFrameworkDetail] = useState<Framework | null>(null)
  const [isLoading, setIsLoading] = useState<boolean>(false)
  const [error, setError] = useState<string | null>(null)


  useEffect(() => {
    const fetch = async () => {
      const frameworksData = await getFrameworks();
      console.log(frameworksData)
      setFrameworks(frameworksData)
    }
    fetch()
  }, [])


  useEffect(() => {
    const fetch = async () => {
      const frameworkData = await getFramework(selected)
      console.log(frameworkData)
      setFrameworkDetail(frameworkData)
    }
    fetch()
  }, [selected])


  const handleGenerate = async () => {
    setIsLoading(true)
    try {
      const parsed = JSON.parse(json)
      const payload = { ...parsed, framework: selected }
      const projectTitle = parsed.project_name
      const blob = await generateProject(payload)
  
      const safeName = projectTitle.replace(/[<>:"/\\|?*]+/g, "_")
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")
      a.href = url
      a.download = `${safeName}.tar.gz`
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      setTimeout(() => URL.revokeObjectURL(url), 1000)
  
    } catch (err) {
      if (err instanceof SyntaxError) {
        setError("JSON inválido")
      } else {
        console.error(err)
        setError("Erro ao gerar projeto")
      }
    } finally {
      setIsLoading(false)
    }
  }



  return (
    <div className={styles.app}>
      <header className={styles.header}>
        <h1 className={styles.title}>RailForge</h1>
        <p className={styles.subtitle}>Generate production-ready APIs from a JSON definition</p>
      </header>
  
      <main className={styles.main}>
        <aside className={styles.sidebar}>
          <FrameworkSelector
            selected={selected}
            frameworks={frameworks}
            onChange={setSelected}
          />
          <div>
          <button 
              className={styles.button} 
              onClick={handleGenerate}
              disabled={isLoading}
            >
              {isLoading ? "Generating..." : "Download"}
            </button>
            {error && <p className={styles.error}>{error}</p>}
          </div>
        </aside>
  
        <section className={styles.editor}>
          <ModelEditor 
            value={json} 
            onChange={v => { setJson(v); setError(null) }} 
          />
        </section>
  
        <aside className={styles.reference}>
          <ReferencePanel
            acceptedTypes={frameworkDetail?.accepted_types ?? []}
            generates={frameworkDetail?.generates ?? []}
          />
        </aside>
      </main>
  
    </div>
  )
}

export default App
