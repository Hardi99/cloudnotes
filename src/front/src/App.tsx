import { useState, useEffect } from 'react'

const API_URL = import.meta.env.VITE_API_URL ?? 'http://localhost:80'

interface Note {
  id: string
  title: string
  content: string
  createdAt: string
}

export default function App() {
  const [notes, setNotes] = useState<Note[]>([])
  const [title, setTitle] = useState('')
  const [content, setContent] = useState('')
  const [loading, setLoading] = useState(false)

  const fetchNotes = async () => {
    const res = await fetch(`${API_URL}/notes`)
    const data = await res.json()
    setNotes(data)
  }

  useEffect(() => { fetchNotes() }, [])

  const createNote = async (e: React.FormEvent) => {
    e.preventDefault()
    if (!title.trim()) return
    setLoading(true)
    await fetch(`${API_URL}/notes`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ title, content })
    })
    setTitle('')
    setContent('')
    await fetchNotes()
    setLoading(false)
  }

  const deleteNote = async (id: string) => {
    await fetch(`${API_URL}/notes/${id}`, { method: 'DELETE' })
    await fetchNotes()
  }

  return (
    <div className="container">
      <h1>CloudNotes</h1>

      <form onSubmit={createNote} className="form">
        <input
          placeholder="Titre"
          value={title}
          onChange={e => setTitle(e.target.value)}
          required
        />
        <textarea
          placeholder="Contenu..."
          value={content}
          onChange={e => setContent(e.target.value)}
          rows={3}
        />
        <button type="submit" disabled={loading}>
          {loading ? 'Création...' : 'Ajouter'}
        </button>
      </form>

      <div className="notes">
        {notes.map(note => (
          <div key={note.id} className="note">
            <div className="note-header">
              <h3>{note.title}</h3>
              <button onClick={() => deleteNote(note.id)} className="delete">×</button>
            </div>
            <p>{note.content}</p>
            <small>{new Date(note.createdAt).toLocaleString('fr-FR')}</small>
          </div>
        ))}
      </div>
    </div>
  )
}
