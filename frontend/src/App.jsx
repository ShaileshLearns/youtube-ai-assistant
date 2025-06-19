import { useState } from 'react';
import axios from 'axios';
import './App.css';

function App() {
  const [url, setUrl] = useState('');
  const [transcript, setTranscript] = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSubmit = async (e) => {
    e.preventDefault();
    setTranscript('');
    setError('');
    setLoading(true);

    try {
      const response = await axios.post(
        'http://127.0.0.3:8000/transcribe/',
        new URLSearchParams({ url }),
        { headers: { 'Content-Type': 'application/x-www-form-urlencoded' } }
      );
      setTranscript(response.data.transcript);
    } catch (err) {
      setError(err.response?.data?.detail || "Something went wrong.");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ padding: '20px' }}>
      <h1>YouTube Transcript Generator</h1>
      <form onSubmit={handleSubmit}>
        <input
          type="text"
          placeholder="Enter YouTube URL"
          value={url}
          onChange={(e) => setUrl(e.target.value)}
          style={{ width: '400px', padding: '8px' }}
        />
        <button type="submit" style={{ marginLeft: '10px' }}>Get Transcript</button>
      </form>

      {loading && <p>Processing...</p>}
      {error && <p style={{ color: 'red' }}>{error}</p>}
      {transcript && (
        <textarea value={transcript} readOnly rows={20} cols={80} />
      )}
    </div>
  );
}

export default App;
