
import { useState } from 'react'
import './App.css'

function App() {
  const [question, setQuestion] = useState('')
  const [messages, setMessages] = useState([])
  const [loading, setLoading] = useState(false)

  const [file, setFile] = useState(null)
  const [uploading, setUploading] = useState(false)
  const [uploadStatus, setUploadStatus] = useState('')

  const uploadPDF = async (e) => {
    e.preventDefault()

    if (!file || uploading) return

    setUploading(true)
    setUploadStatus('Uploading and processing PDF...')

    const formData = new FormData()
    formData.append('file', file)

    try {
      const response = await fetch('/upload', {
        method: 'POST',
        body: formData
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'PDF upload failed')
      }

      setUploadStatus(
        `Successfully uploaded ${data.filename} (${data.chunks} chunks)`
      )
      setFile(null)
      e.target.reset()

    } catch (error) {
      setUploadStatus(error.message)
    } finally {
      setUploading(false)
    }
  }

  const sendMessage = async (e) => {
    e.preventDefault()

    if (!question.trim() || loading) return

    const userQuestion = question.trim()

    setMessages(prev => [
      ...prev,
      { role: 'user', content: userQuestion }
    ])

    setQuestion('')
    setLoading(true)

    try {
      const response = await fetch('/chat', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json'
        },
        body: JSON.stringify({ question: userQuestion })
      })

      const data = await response.json()

      if (!response.ok) {
        throw new Error(data.detail || 'Failed to get chatbot response')
      }

      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: data.answer,
          sources: data.sources || []
        }
      ])

    } catch (error) {
      setMessages(prev => [
        ...prev,
        {
          role: 'assistant',
          content: error.message || 'Sorry, something went wrong.'
        }
      ])
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <aside className="sidebar">
        <h2>PDF Assistant</h2>

        <button onClick={() => setMessages([])}>
          + New Chat
        </button>

        <p>Ask questions about your documents.</p>

        <hr />

        <h3>Upload PDF</h3>

        <form onSubmit={uploadPDF}>
          <input
            type="file"
            accept=".pdf,application/pdf"
            onChange={e => {
              setFile(e.target.files?.[0] || null)
              setUploadStatus('')
            }}
          />

          <button
            type="submit"
            disabled={!file || uploading}
          >
            {uploading ? 'Uploading...' : 'Upload PDF'}
          </button>
        </form>

        {uploadStatus && (
          <p>{uploadStatus}</p>
        )}
      </aside>

      <main className="main">
        <header>
          <h2>Personal PDF Chatbot</h2>
          <span>Powered by RAG</span>
        </header>

        <section className="chat">
          {messages.length === 0 && (
            <div className="welcome">
              <h1>Welcome to PDF Assistant</h1>
              <p>Upload a PDF and ask questions about it.</p>

              <div className="suggestions">
                <button onClick={() =>
                  setQuestion('Tell me about my DevOps projects')
                }>
                  My DevOps projects
                </button>

                <button onClick={() =>
                  setQuestion('What cloud technologies do I know?')
                }>
                  My cloud skills
                </button>
              </div>
            </div>
          )}

          {messages.map((msg, index) => (
            <div className={`message ${msg.role}`} key={index}>
              <strong>
                {msg.role === 'user' ? 'You' : 'PDF Assistant'}
              </strong>

              <p>{msg.content}</p>

              {msg.sources?.length > 0 && (
                <details>
                  <summary>View PDF sources</summary>

                  {msg.sources.map((source, i) => (
                    <div className="source" key={i}>
                      <strong>{source.filename}</strong>
                      <p>Page: {source.page}</p>
                      <p>{source.text}</p>
                    </div>
                  ))}
                </details>
              )}
            </div>
          ))}

          {loading && (
            <div className="loading">
              Searching your PDFs...
            </div>
          )}
        </section>

        <form className="input-area" onSubmit={sendMessage}>
          <input
            value={question}
            onChange={e => setQuestion(e.target.value)}
            placeholder="Ask something about your PDF..."
            disabled={loading}
          />

          <button
            type="submit"
            disabled={loading || !question.trim()}
          >
            Send
          </button>
        </form>
      </main>
    </div>
  )
}

export default App

