import { useState } from 'react'
import axios from 'axios'
import './App.css'

/** Classify each line of `newText` as unchanged vs added vs changed vs replaced (vs original). */
function classifySuggestedLines(originalText, newText) {
  const oldLines = String(originalText || '').split('\n')
  const newLines = String(newText || '').split('\n')
  const m = oldLines.length
  const n = newLines.length
  const dp = Array.from({ length: m + 1 }, () => new Array(n + 1).fill(0))
  for (let i = m - 1; i >= 0; i--) {
    for (let j = n - 1; j >= 0; j--) {
      dp[i][j] =
        oldLines[i] === newLines[j] ? dp[i + 1][j + 1] + 1 : Math.max(dp[i + 1][j], dp[i][j + 1])
    }
  }
  const flags = new Array(n).fill('added')
  let i = 0
  let j = 0
  while (i < m && j < n) {
    if (oldLines[i] === newLines[j]) {
      flags[j] = 'unchanged'
      i++
      j++
    } else if (dp[i + 1][j] >= dp[i][j + 1]) {
      i++
    } else {
      j++
    }
  }
  return newLines.map((text, index) => ({
    text,
    kind: flags[index] === 'unchanged' ? 'unchanged' : 'added',
  }))
}

function CodeBlock({ code, lineKinds = null }) {
  const lines = String(code || '').split('\n')
  return (
    <div className="code-block">
      {lines.map((line, index) => {
        const kind = lineKinds?.[index] ?? 'neutral'
        const lineClass =
          kind === 'added'
            ? 'code-line code-line--added'
            : kind === 'unchanged'
              ? 'code-line code-line--unchanged'
              : 'code-line'
        return (
          <div className={lineClass} key={index}>
            <span className="line-number">{index + 1}</span>
            <span className="line-content">{line || '\u200B'}</span>
          </div>
        )
      })}
    </div>
  )
}

function SuggestedCodeBlock({ originalCode, suggestedCode }) {
  const classified = classifySuggestedLines(originalCode, suggestedCode)
  const lines = classified.map((c) => c.text)
  const kinds = classified.map((c) => c.kind)
  return <CodeBlock code={lines.join('\n')} lineKinds={kinds} />
}

function App() {
  const [repoUrl, setRepoUrl] = useState('')
  const [bugDescription, setBugDescription] = useState('')
  const [applyFixes, setApplyFixes] = useState(true)
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
        apply_fixes: applyFixes
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
        <label className="checkbox-row">
          <input
            type="checkbox"
            checked={applyFixes}
            onChange={(e) => setApplyFixes(e.target.checked)}
          />
          <span>Apply suggested fixes to the cloned repository (new git branch)</span>
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
          {results.repo_path && (
            <p>
              <strong>Local clone:</strong>{' '}
              <span className="bug-location-path">{results.repo_path}</span>
            </p>
          )}
          {results.fix_branch && (
            <p>
              <strong>Fix branch:</strong>{' '}
              <span className="bug-location-path">{results.fix_branch}</span>
            </p>
          )}

          <h2>Files Scanned</h2>
          <p>{results.files_scanned} files were scanned for potential issues.</p>

          <h2>Relevant Files</h2>
          <ul>
            {results.relevant_files.map((file, index) => (
              <li key={index}>{file}</li>
            ))}
          </ul>

          <h2>Bug Locations</h2>
          <ul className="bug-locations-list">
            {results.suggested_fixes.map((fix, index) => (
              <li key={index}>
                <span className="bug-location-path">
                  {fix.file}:{fix.line}
                </span>
              </li>
            ))}
          </ul>

          <h2>AI Suggested Fix</h2>
          {results.suggested_fixes.map((fix, index) => (
            <details key={index} className="bug-location-card">
              <summary className="bug-location-summary">
                <span className="bug-location-summary-label">
                  Bug Location {index + 1}:
                </span>
                <span className="bug-location-summary-path">
                  {fix.file}:{fix.line}
                </span>
                {results.apply_fixes && (
                  <span
                    className={
                      fix.fix_applied ? 'fix-applied-badge' : 'fix-not-applied-badge'
                    }
                  >
                    {fix.fix_applied ? 'Applied to repo' : 'Not applied'}
                  </span>
                )}
              </summary>
              <div className="bug-location-content">
                <div className="code-section">
                  <h4>Original Code</h4>
                  <CodeBlock code={fix.original_code} />
                </div>
                <div className="code-section code-section--suggested">
                  <h4>AI Suggested Fix</h4>
                  {fix.suggested_fix ? (
                    <SuggestedCodeBlock
                      originalCode={fix.original_code}
                      suggestedCode={fix.suggested_fix}
                    />
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
