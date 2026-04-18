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

function NewBranchSwitch({ checked, onChange, disabled }) {
  return (
    <button
      type="button"
      role="switch"
      aria-checked={checked}
      aria-label="Apply fixes on a new git branch"
      disabled={disabled}
      className={`new-branch-switch${checked ? ' new-branch-switch--on' : ''}`}
      onClick={() => onChange(!checked)}
    >
      <span className="new-branch-switch__thumb" aria-hidden />
    </button>
  )
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
        apply_fixes: applyFixes,
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
      <header className="app-header">
        <div className="app-header__brand">
          <span className="app-logo" aria-hidden>
            ◈
          </span>
          <div>
            <p className="app-kicker">Autonomous repair</p>
            <h1 className="app-title">AI Bug Fixer</h1>
          </div>
        </div>
        <div className="app-header__pills" aria-label="Workflow">
          <span className="pill">Scan</span>
          <span className="pill pill--accent">Suggest</span>
          <span className="pill">Ship</span>
        </div>
      </header>

      <div className="layout-grid">
        <section className="panel panel--form" aria-labelledby="run-heading">
          <h2 id="run-heading" className="panel__title">
            Run an analysis
          </h2>
          <p className="panel__lede">
            Drop a repo link, describe the glitchy behavior, and let the model hunt likely hotspots.
          </p>

          <div className="field">
            <label className="field__label" htmlFor="repo-url">
              GitHub repository URL
            </label>
            <input
              id="repo-url"
              className="field__input"
              type="url"
              inputMode="url"
              autoComplete="url"
              value={repoUrl}
              onChange={(e) => setRepoUrl(e.target.value)}
              placeholder="https://github.com/you/cool-app"
            />
          </div>

          <div className="field">
            <label className="field__label" htmlFor="bug-desc">
              Bug description
            </label>
            <textarea
              id="bug-desc"
              className="field__input field__input--textarea"
              value={bugDescription}
              onChange={(e) => setBugDescription(e.target.value)}
              placeholder="Repro steps, expected vs actual, errors in console…"
              rows={5}
            />
          </div>

          <div className="branch-card">
            <div className="branch-card__header">
              <div>
                <h3 className="branch-card__title">New branch workflow</h3>
                <p className="branch-card__subtitle">
                  When enabled, fixes are written on a fresh git branch in the cloned repo — not on your
                  default branch.
                </p>
              </div>
              <NewBranchSwitch
                checked={applyFixes}
                onChange={setApplyFixes}
                disabled={loading}
              />
            </div>
            <p className={`branch-card__status${applyFixes ? ' is-on' : ''}`}>
              {applyFixes
                ? 'On — patches land on an isolated fix branch after analysis.'
                : 'Off — analysis only; nothing is committed to a new branch.'}
            </p>
          </div>

          <button
            type="button"
            className="cta"
            onClick={handleAnalyze}
            disabled={loading}
          >
            <span className="cta__shine" aria-hidden />
            {loading ? 'Running analysis…' : 'Analyze bug'}
          </button>
        </section>

        <aside className="panel panel--aside" aria-label="Tips">
          <h2 className="panel__title">Make it hit different</h2>
          <ul className="tip-list">
            <li>
              <strong>Be specific.</strong> Mention files, endpoints, or error strings if you know them.
            </li>
            <li>
              <strong>Public repos</strong> work best for quick clones — keep tokens out of the URL field.
            </li>
            <li>
              <strong>New branch mode</strong> is ideal when you still want main untouched while you review
              diffs.
            </li>
          </ul>
          <div className="aside-glow" aria-hidden />
        </aside>
      </div>

      {results && (
        <section className="results" aria-label="Analysis results">
          <div className="results__intro">
            <h2 className="results__heading">Results</h2>
            <p className="results__meta">
              {results.repo && (
                <>
                  <span className="meta-chip">{results.repo}</span>
                  {results.fix_branch && (
                    <span className="meta-chip meta-chip--branch">{results.fix_branch}</span>
                  )}
                </>
              )}
            </p>
          </div>

          <div className="results-grid">
            <article className="result-card">
              <h3 className="result-card__title">Repository</h3>
              <p className="result-card__body">
                <strong>Bug:</strong> {results.bug}
              </p>
              {results.repo_path && (
                <p className="result-card__body">
                  <strong>Local clone:</strong>{' '}
                  <span className="bug-location-path">{results.repo_path}</span>
                </p>
              )}
              {results.fix_branch && (
                <p className="result-card__body">
                  <strong>Fix branch:</strong>{' '}
                  <span className="bug-location-path">{results.fix_branch}</span>
                </p>
              )}
              {results.test_results && (
                <p className="result-card__body">
                  <strong>Test status:</strong> {results.test_results.status}
                </p>
              )}
              {results.push_status && (
                <p className="result-card__body">
                  <strong>Push status:</strong> {results.push_status}
                </p>
              )}
              {results.fix_summary_file && (
                <p className="result-card__body">
                  <strong>Branch summary file:</strong>{' '}
                  <span className="bug-location-path">{results.fix_summary_file}</span>
                </p>
              )}
            </article>

            <article className="result-card">
              <h3 className="result-card__title">Scan overview</h3>
              <p className="result-card__body">{results.files_scanned} files scanned.</p>
              <h4 className="result-card__subtitle">Relevant files</h4>
              <ul className="result-list">
                {results.relevant_files.map((file, index) => (
                  <li key={index}>{file}</li>
                ))}
              </ul>
            </article>

            <article className="result-card result-card--wide">
              <h3 className="result-card__title">Bug locations</h3>
              <ul className="bug-locations-list">
                {results.suggested_fixes.map((fix, index) => (
                  <li key={index}>
                    <span className="bug-location-path">
                      {fix.file}:{fix.line}
                    </span>
                  </li>
                ))}
              </ul>
            </article>
          </div>

          <h2 className="results__section-title">AI suggested fixes</h2>
          {results.suggested_fixes.map((fix, index) => (
            <details key={index} className="bug-location-card">
              <summary className="bug-location-summary">
                <span className="bug-location-summary-label">Bug location {index + 1}</span>
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
                  <h4>Original code</h4>
                  <CodeBlock code={fix.original_code} />
                </div>
                <div className="code-section code-section--suggested">
                  <h4>AI suggested fix</h4>
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
        </section>
      )}
    </div>
  )
}

export default App
