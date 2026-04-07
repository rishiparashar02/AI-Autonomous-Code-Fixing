import { useState } from 'react'
import axios from 'axios'
import './App.css'

function CodeBlock({ code }) {
  const lines = String(code || '').split('\n')
  return (
    <div className="code-block">
      {lines.map((line, index) => (
        <div className="code-line" key={index}>
          <span className="line-number">{index + 1}</span>
          <span className="line-content">{line || '\u200B'}</span>
        </div>
      ))}
    </div>
  )
}

function App() {
  const [repoUrl, setRepoUrl] = useState('')
  const [bugDescription, setBugDescription] = useState('')
  const [results, setResults] = useState(null)
  const [loading, setLoading] = useState(false)

  const handleAnalyze = async () => {
    if (!repoUrl || !bugDescription) {
      alert('Please fill in both fields.')
      return
    }
    setLoading(true)
    try {
      const response = await axios.post('http://localhost:8000/analyze-bug', {
        repo_url: repoUrl,
        bug_description: bugDescription,
        apply_fixes: false
      })
      setResults(response.data)
    } catch (error) {
      console.error('Error analyzing bug:', error)
      alert('Error analyzing bug. Check console for details.')
    } finally {
      setLoading(false)
    }
  }

  return (
    <div className="app">
      <h1>AI Autonomous Bug Fixing System</h1>
      <div className="input-section">
        <label>
          GitHub Repository URL:
          <input
            type="text"
            value={repoUrl}
            onChange={(e) => setRepoUrl(e.target.value)}
            placeholder="https://github.com/user/repo"
          />
        </label>
        <label>
          Bug Description:
          <textarea
            value={bugDescription}
            onChange={(e) => setBugDescription(e.target.value)}
            placeholder="Describe the bug..."
          />
        </label>
        <button onClick={handleAnalyze} disabled={loading}>
          {loading ? 'Analyzing...' : 'Analyze Bug'}
        </button>
      </div>

      {results && (
        <div className="results">
          <h2>Repository Info</h2>
          <p><strong>Repository:</strong> {results.repo}</p>
          <p><strong>Bug:</strong> {results.bug}</p>

          <h2>Files Scanned</h2>
          <p>{results.files_scanned} files were scanned for potential issues.</p>

          <h2>Relevant Files</h2>
          <ul>
            {results.relevant_files.map((file, index) => (
              <li key={index}>{file}</li>
            ))}
          </ul>

          <h2>Bug Locations</h2>
          <ul>
            {results.suggested_fixes.map((fix, index) => (
              <li key={index}>{fix.file}:{fix.line}</li>
            ))}
          </ul>

          <h2>AI Suggested Fix</h2>
          {results.suggested_fixes.map((fix, index) => (
            <details key={index} className="bug-location-card">
              <summary className="bug-location-summary">
                Bug Location {index + 1}: {fix.file}:{fix.line}
              </summary>
              <div className="bug-location-content">
                <div className="code-section">
                  <h4>Original Code</h4>
                  <CodeBlock code={fix.original_code} />
                </div>
                <div className="code-section">
                  <h4>AI Suggested Fix</h4>
                  {fix.suggested_fix ? (
                    <CodeBlock code={fix.suggested_fix} />
                  ) : (
                    <div className="error-note">
                      No AI suggestion was returned.
                      {fix.error ? ` Error: ${fix.error}` : ''}
                    </div>
                  )}
                </div>
                {fix.diff && (
                  <div className="code-section">
                    <h4>Diff</h4>
                    <CodeBlock code={fix.diff} />
                  </div>
                )}
                {fix.patch && !fix.diff && (
                  <div className="code-section">
                    <h4>Patch</h4>
                    <CodeBlock code={fix.patch} />
                  </div>
                )}
              </div>
            </details>
          ))}
        </div>
      )}
    </div>
  )
}

export default App
