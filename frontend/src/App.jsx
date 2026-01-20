import { useState } from "react";
import "./App.css";
import logo from "./assets/logo.png";

// Use environment variable or fallback to Render deployment
const API_BASE = import.meta.env.VITE_API_BASE || "https://codeclutch-backend.onrender.com";

function App() {
  // State management for user input and API responses
  const [resumeText, setResumeText] = useState("");
  const [skills, setSkills] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");
  const [activeStep, setActiveStep] = useState(1);

  // Helper function to make API calls with error handling
  const makeApiCall = async (endpoint, payload) => {
    try {
      const response = await fetch(`${API_BASE}${endpoint}`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(payload),
      });

      if (!response.ok) {
        const errorData = await response.json().catch(() => ({}));
        throw new Error(errorData.detail || `HTTP ${response.status}: Request failed`);
      }

      return await response.json();
    } catch (err) {
      throw new Error(err.message || "Network request failed. Please check your connection.");
    }
  };

  // Step 1: Send resume to backend to extract skills
  const analyzeResume = async () => {
    if (!resumeText.trim()) {
      setError("Please paste your resume before proceeding.");
      return;
    }

    setError("");
    setLoading(true);
    try {
      const data = await makeApiCall("/analyze-resume", { resume_text: resumeText });
      setSkills(data.skills || []);
      setActiveStep(2);
    } catch (err) {
      setError(`Resume analysis failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Step 2: Generate interview questions based on detected skills
  const generateQuestions = async () => {
    if (!skills || skills.length === 0) {
      setError("No skills to generate questions for. Please analyze your resume first.");
      return;
    }

    setError("");
    setLoading(true);
    try {
      const data = await makeApiCall("/generate-questions", { skills });
      setQuestions(data.questions || []);
      setAnswers({});
      setActiveStep(3);
    } catch (err) {
      setError(`Question generation failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Step 3: Submit user answers and receive AI-powered feedback
  const submitAnswers = async () => {
    const unansweredCount = questions.filter((q) => !answers[q.question]?.trim()).length;
    if (unansweredCount > 0) {
      setError(`Please answer all ${unansweredCount > 1 ? unansweredCount + " questions" : "question"} before submitting.`);
      return;
    }

    setError("");
    setLoading(true);
    try {
      const qa_pairs = questions.map((q) => ({
        question: q.question,
        answer: answers[q.question] || "",
      }));

      const data = await makeApiCall("/evaluate-answers", { qa_pairs });
      setFeedback(data);
      setActiveStep(4);
    } catch (err) {
      setError(`Answer evaluation failed: ${err.message}`);
    } finally {
      setLoading(false);
    }
  };

  // Reset the entire flow
  const startOver = () => {
    setResumeText("");
    setSkills([]);
    setQuestions([]);
    setAnswers({});
    setFeedback(null);
    setError("");
    setActiveStep(1);
  };

  // Main UI: Renders the interview prep flow
  return (
    <div className="app-shell">
      <div className="container">
        <div className="brand">
          <img src={logo} alt="CodeClutch logo" className="logo-img" />
          <div>
            <h1>CodeClutch</h1>
            <p className="tagline">AI-powered interview preparation for software engineers</p>
          </div>
        </div>

        {/* Error display */}
        {error && <div className="error">⚠️ {error}</div>}

        {/* Loading indicator */}
        {loading && (
          <div className="loading-indicator">
            <div className="spinner"></div>
            <span>Processing your request...</span>
          </div>
        )}

        {/* Section 1: Resume input */}
        {activeStep >= 1 && (
          <>
            <h3>Step 1: Upload Your Resume</h3>
            <textarea
              placeholder="Paste your resume text here (include skills, experience, projects)"
              value={resumeText}
              onChange={(e) => setResumeText(e.target.value)}
              disabled={loading}
              rows={8}
            />
            <button 
              onClick={analyzeResume} 
              disabled={loading || !resumeText.trim()}
            >
              {loading ? "Analyzing..." : "Extract Skills"}
            </button>
          </>
        )}

        {/* Section 2: Display extracted skills and prompt for questions */}
        {skills.length > 0 && activeStep >= 2 && (
          <>
            <h3>Step 2: Your Detected Skills</h3>
            <div className="skills-list">
              <ul>
                {skills.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>
            <button 
              onClick={generateQuestions} 
              disabled={loading}
            >
              {loading ? "Generating..." : "Generate Interview Questions"}
            </button>
          </>
        )}

        {/* Section 3: Interview questions and user answers */}
        {questions.length > 0 && activeStep >= 3 && (
          <>
            <h3>Step 3: Answer Interview Questions</h3>
            <p style={{ marginBottom: "1rem" }}>
              Please provide thoughtful answers to each question below:
            </p>
            {questions.map((q, i) => (
              <div key={i} className="question-block">
                <p>
                  <strong>Q{i + 1}. {q.question}</strong>
                </p>
                <p style={{ fontSize: "0.85rem", color: "#64748b", marginBottom: "0.75rem" }}>
                  Difficulty: <span style={{ fontWeight: 600, color: "#475569" }}>{q.difficulty}</span> • 
                  Focus: <span style={{ fontWeight: 600, color: "#475569" }}>{q.skill_focus}</span>
                </p>
                <textarea
                  rows={3}
                  placeholder="Type your answer here..."
                  value={answers[q.question] || ""}
                  onChange={(e) =>
                    setAnswers({ ...answers, [q.question]: e.target.value })
                  }
                  disabled={loading}
                />
              </div>
            ))}
            <button 
              onClick={submitAnswers} 
              disabled={loading}
            >
              {loading ? "Evaluating..." : "Get AI Feedback"}
            </button>
          </>
        )}

        {/* Section 4: Feedback results and performance summary */}
        {feedback && activeStep >= 4 && (
          <>
            <h3>Step 4: Your Interview Performance</h3>

            {/* Individual question feedback */}
            {feedback.evaluations.map((e, i) => (
              <div key={i} className="feedback-block">
                <div style={{ display: "flex", alignItems: "center", gap: "1rem", marginBottom: "0.75rem" }}>
                  <p style={{ margin: 0, flex: 1 }}>
                    <strong>Q{i + 1}. {e.question}</strong>
                  </p>
                  <div className="score-display">{e.score}/10</div>
                </div>
                <p style={{ color: "#475569", lineHeight: "1.7" }}>{e.feedback}</p>
              </div>
            ))}

            {/* Strengths section */}
            <h4>💪 What You Did Well</h4>
            <div className="strengths-list">
              <ul>
                {feedback.strengths.map((s, i) => (
                  <li key={i}>{s}</li>
                ))}
              </ul>
            </div>

            {/* Improvements section */}
            <h4>🎯 Areas to Focus On</h4>
            <div className="improvements-list">
              <ul>
                {feedback.improvements.map((i, idx) => (
                  <li key={idx}>{i}</li>
                ))}
              </ul>
            </div>

            {/* Overall readiness */}
            <div style={{ 
              padding: "1.5rem", 
              background: "linear-gradient(135deg, #f0f7ff, #e0f2fe)", 
              border: "1px solid #bfdbfe", 
              borderRadius: "12px",
              marginTop: "1.5rem"
            }}>
              <p style={{ margin: 0, fontSize: "0.95rem", color: "#0c4a6e" }}>
                <strong>📊 Interview Readiness Summary:</strong>
              </p>
              <p style={{ margin: "0.5rem 0 0 0", color: "#0c4a6e", lineHeight: "1.7" }}>
                {feedback.overall_readiness_summary}
              </p>
            </div>

            {/* Start over button */}
            <button 
              onClick={startOver}
              style={{ marginTop: "1.5rem" }}
            >
              🔄 Start New Interview Session
            </button>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
