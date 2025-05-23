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
    formData.append('file', file) // must be 'file' to match backend
    formData.append('time_signature', timeSignature)

    try {
      const res = await fetch('http://localhost:5000/upload', {
        method: 'POST',
        body: formData,
      })

      const data = await res.json()

      if (res.ok) {
        setResponse(`✅ Beat detection started.\nDetected BPM: ${data.detected_bpm || 'N/A'}\n${data.message || ''}`)
      } else {
        setResponse(`❌ Error: ${data.error}`)
      }
    } catch (error) {
      setResponse('❌ Error uploading file. Make sure backend is running.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div style={{ padding: '20px', fontFamily: 'Arial, sans-serif' }}>
      <h2>🎵 Upload Song for Beat Detection</h2>
      <form onSubmit={handleSubmit} style={{ marginBottom: '20px' }}>
        <div style={{ marginBottom: '10px' }}>
          <label><strong>Choose audio file:</strong> </label>
          <input type="file" accept="audio/*" onChange={handleFileChange} />
        </div>
        <div style={{ marginBottom: '10px' }}>
          <label><strong>Time Signature:</strong> </label>
          <input
            type="text"
            value={timeSignature}
            onChange={handleTimeSignatureChange}
            placeholder="e.g. 4/4"
          />
        </div>
        <button type="submit" disabled={loading}>
          {loading ? 'Processing...' : 'Upload & Detect'}
        </button>
      </form>
      {response && (
        <div style={{ whiteSpace: 'pre-wrap', color: response.startsWith('❌') ? 'red' : 'green' }}>
          {response}
        </div>
      )}
    </div>
  )
}

export default App
