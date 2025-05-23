import { useState } from 'react'

function App() {
  const [file, setFile] = useState(null)
  const [timeSignature, setTimeSignature] = useState('4/4')
  const [response, setResponse] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleFileChange = (e) => {
    setFile(e.target.files[0])
  }

  const handleTimeSignatureChange = (e) => {
    setTimeSignature(e.target.value)
  }

  const handleSubmit = async (e) => {
    e.preventDefault()
    if (!file) {
      alert('Please upload a song file.')
      return
    }

    setLoading(true)
    setResponse(null)

    const formData = new FormData()
    formData.append('song', file)
    formData.append('time_signature', timeSignature)

    try {
      const res = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      })

      const data = await res.json()

      if (res.ok) {
        setResponse(`Detected BPM: ${data.detected_bpm}. ${data.message}`)
      } else {
        setResponse(`Error: ${data.error}`)
      }
    } catch (error) {
      setResponse('Error uploading file.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div>
      <h1>Upload Song for Beat Detection</h1>
      <form onSubmit={handleSubmit}>
        <div>
          <label>Choose song (mp3, wav, etc): </label>
          <input type="file" accept="audio/*" onChange={handleFileChange} />
        </div>
        <div>
          <label>Time Signature (e.g. 4/4): </label>
          <input
            type="text"
            value={timeSignature}
            onChange={handleTimeSignatureChange}
            placeholder="e.g. 4/4"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Upload & Process'}
        </button>
      </form>
      {response && (
        <div style={{ marginTop: '20px', whiteSpace: 'pre-wrap' }}>{response}</div>
      )}
    </div>
  )
}

export default App
