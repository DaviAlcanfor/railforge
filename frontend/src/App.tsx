import styles from './styles/App.module.css'

import { Github, Mail, Instagram, Linkedin } from 'lucide-react'

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
    try {
      const parsed = JSON.parse(json)
      const projectTitle = parsed.project_name
      const blob = await generateProject(parsed)

      // remove invalid characters from filename
      const safeName = projectTitle.replace(/[<>:"/\\|?*]+/g, "_")
  
      const url = URL.createObjectURL(blob)
      const a = document.createElement("a")  
      a.href = url
      a.download = `${safeName}.tar.gz`
  
      // some browsers need the elem in the DOM
      document.body.appendChild(a)
      a.click()
      document.body.removeChild(a)
      
      // release the memory when the download begins
      setTimeout(() => URL.revokeObjectURL(url), 1000)
  
    } catch (err) {
      console.error(err)
      alert("JSON inválido")
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
          <button className={styles.button} onClick={handleGenerate}>
            Download
          </button>
        </aside>
  
        <section className={styles.editor}>
          <ModelEditor value={json} onChange={setJson} />
        </section>
  
        <aside className={styles.reference}>
          <ReferencePanel
            acceptedTypes={frameworkDetail?.accepted_types ?? []}
            generates={frameworkDetail?.generates ?? []}
          />
        </aside>
      </main>
  
      <footer className={styles.footer}>
        <button className={styles.button} onClick={handleGenerate}>
          Download
        </button>
        <div className={styles.links}>
          <a href="https://github.com/DaviAlcanfor/" target="_blank" rel="noreferrer"><Github size={16} /></a>
          <a href="mailto:alcanfordavi@gmail.com"><Mail size={16} /></a>
          <a href="https://linkedin.com/in/..." target="_blank" rel="noreferrer"><Linkedin size={16} /></a>
          <a href="https://instagram.com/..." target="_blank" rel="noreferrer"><Instagram size={16} /></a>
        </div>
        <p className={styles.copyright}>© 2026 Davi Alcanfor</p>
      </footer>
    </div>
  )
}

export default App
