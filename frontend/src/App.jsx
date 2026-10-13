
import { useState } from "react";
import {
  Shield, Search, Activity, Globe, AlertTriangle,
  CheckCircle, Network, LoaderCircle, Terminal,
  ArrowUpRight, Radar
} from "lucide-react";
import "./App.css";

const API = "http://127.0.0.1:5000";

function cleanMarkdown(text = "") {
  return text
    .replace(/\\([#*`])/g, "$1")
    .replace(/^#{1,6}\s*/gm, "")
    .replace(/\*\*(.*?)\*\*/g, "$1")
    .replace(/__(.*?)__/g, "$1")
    .trim();
}

function App() {
  const [ip, setIp] = useState("");
  const [behavior, setBehavior] = useState("");
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [report, setReport] = useState(null);

  async function investigate(e) {
    e.preventDefault();
    setLoading(true);
    setError("");
    setReport(null);

    try {
      const response = await fetch(`${API}/api/investigate`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ ip: ip.trim(), behavior: behavior.trim() })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.error || "Investigation failed.");
      }

      setReport(data);
    } catch (err) {
      setError(
        err.message === "Failed to fetch"
          ? "Cannot connect to Flask. Check that the backend is running on port 5000."
          : err.message
      );
    } finally {
      setLoading(false);
    }
  }

  const interpretation = cleanMarkdown(report?.interpretation || "");
  const riskMatch = interpretation.match(/\b(LOW|MEDIUM|HIGH)\b/i);
  const risk = riskMatch ? riskMatch[1].toUpperCase() : "REVIEW";

  return (
    <div className="app-shell">
      <aside className="sidebar">
        <div className="brand">
          <div className="brand-icon"><Shield size={27} /></div>
          <div className="brand-copy">
            <strong>Agentic Threat<br />Intelligence</strong>
            <span>CYBERSECURITY PLATFORM</span>
          </div>
        </div>

        <div className="nav-label">WORKSPACE</div>
        <div className="nav-item active">
          <Activity size={20} />
          <span>Investigation</span>
        </div>
        <div className="nav-item">
          <Network size={20} />
          <span>Agent overview</span>
        </div>

        <div className="sidebar-bottom">
          <span className="status-dot" />
          <div>
            <strong>Local environment</strong>
            <span>Multi-agent system</span>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <div className="eyebrow">SECURITY OPERATIONS / CTI</div>
            <h1>Threat Investigation</h1>
            <p className="topbar-subtitle">
              Investigate indicators and correlate threat intelligence.
            </p>
          </div>
          <div className="workspace-status">
            <span className="status-dot" />
            LOCAL WORKSPACE
          </div>
        </header>

        <section className="welcome">
          <div className="welcome-copy">
            <div className="eyebrow">MULTI-AGENT ANALYSIS</div>
            <h2>Investigate an indicator.</h2>
            <p>
              Analyse IP reputation, abuse reports, and observed attacker
              behaviour through your multi-agent CTI framework.
            </p>
          </div>
          <div className="welcome-icon"><Shield size={48} strokeWidth={1.4} /></div>
        </section>

        <section className="panel search-panel">
          <div className="section-heading">
            <div className="heading-icon"><Radar size={22} /></div>
            <div>
              <h3>New investigation</h3>
              <p>Provide an indicator and, optionally, observed behaviour.</p>
            </div>
          </div>

          <form onSubmit={investigate}>
            <div className="form-field">
              <label htmlFor="ip">
                IP ADDRESS <span className="required-label">REQUIRED</span>
              </label>
              <div className="input-wrap">
                <Globe size={21} />
                <input
                  id="ip"
                  type="text"
                  value={ip}
                  onChange={(e) => setIp(e.target.value)}
                  placeholder="Enter an IP address, e.g. 8.8.8.8"
                  required
                />
              </div>
            </div>

            <div className="form-field">
              <label htmlFor="behavior">
                OBSERVED ATTACKER BEHAVIOUR
                <span className="optional-label">OPTIONAL</span>
              </label>
              <textarea
                id="behavior"
                value={behavior}
                onChange={(e) => setBehavior(e.target.value)}
                placeholder="Describe observed behaviour, e.g. The attacker used PowerShell to execute commands."
                rows={5}
              />
              <p className="field-help">
                Providing observed behaviour enables the MITRE ATT&CK mapping agent.
                An IP address alone is not sufficient to identify an attack technique.
              </p>
            </div>

            <button className="investigate-btn" type="submit" disabled={loading}>
              {loading ? (
                <>
                  <LoaderCircle className="spin" size={21} />
                  Investigating...
                </>
              ) : (
                <>
                  <Search size={21} />
                  Run investigation
                  <ArrowUpRight size={19} />
                </>
              )}
            </button>

            <p className="form-note">
              <Activity size={15} />
              Live intelligence lookups may take a little time.
            </p>
          </form>
        </section>

        {error && (
          <div className="error-box">
            <AlertTriangle size={22} />
            <div>
              <strong>Investigation failed</strong>
              <p>{error}</p>
            </div>
          </div>
        )}

        {loading && (
          <section className="panel loading-box">
            <LoaderCircle className="spin loading-icon" size={30} />
            <div>
              <h3>Investigation in progress</h3>
              <p>
                Collecting intelligence, checking reputation, and preparing
                the analyst assessment. This may take a little time.
              </p>
            </div>
          </section>
        )}

        {report && (
          <section className="results">
            <div className="results-heading">
              <div>
                <div className="eyebrow">INVESTIGATION RESULTS</div>
                <h2>{report.ip}</h2>
                <p>Threat intelligence collected for this indicator.</p>
              </div>
              <div className={`risk-badge ${risk.toLowerCase()}`}>
                <span className="risk-indicator" />
                {risk === "REVIEW" ? "REVIEW REQUIRED" : `${risk} RISK`}
              </div>
            </div>

            <div className="result-grid">
              <article className="panel result-card">
                <div className="card-heading">
                  <div className="card-icon"><Shield size={23} /></div>
                  <div>
                    <h3>VirusTotal</h3>
                    <p>IP reputation intelligence</p>
                  </div>
                </div>
                <pre>{report.virustotal}</pre>
                <div className="source-note">SOURCE / VIRUSTOTAL</div>
              </article>

              <article className="panel result-card">
                <div className="card-heading">
                  <div className="card-icon"><Activity size={23} /></div>
                  <div>
                    <h3>AbuseIPDB</h3>
                    <p>Abuse and reporting intelligence</p>
                  </div>
                </div>
                <pre>{report.abuseipdb}</pre>
                <div className="source-note">SOURCE / ABUSEIPDB</div>
              </article>

              <article className="panel result-card">
                <div className="card-heading">
                  <div className="card-icon"><Network size={23} /></div>
                  <div>
                    <h3>MITRE ATT&CK</h3>
                    <p>Observed behaviour mapping</p>
                  </div>
                </div>
                <pre>{report.mitre}</pre>
                <div className="source-note">SOURCE / MITRE ATT&CK</div>
              </article>

              <article className="panel result-card analyst-card">
                <div className="card-heading">
                  <div className="card-icon"><CheckCircle size={23} /></div>
                  <div>
                    <h3>Analyst assessment</h3>
                    <p>Correlated evidence and overall risk assessment</p>
                  </div>
                  <span className={`mini-risk ${risk.toLowerCase()}`}>
                    {risk}
                  </span>
                </div>
                <div className="interpretation-text">{interpretation}</div>
              </article>
            </div>
          </section>
        )}

        {!report && !loading && (
          <section className="empty-state">
            <div className="empty-icon"><Terminal size={30} /></div>
            <h3>Ready to investigate</h3>
            <p>
              Submit an IP address to view evidence from your CTI agents
              and generate a threat assessment.
            </p>
          </section>
        )}

        <footer>
          AGENTIC THREAT INTELLIGENCE
          <span>•</span>
          MULTI-AGENT CTI FRAMEWORK
        </footer>
      </main>
    </div>
  );
}

export default App;
