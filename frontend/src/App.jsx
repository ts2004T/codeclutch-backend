import { useState } from "react";
import "./App.css";
import logo from "./assets/logo.png";

const API_BASE = "https://codeclutch-backend.onrender.com";

function App() {
  // State management for user input and API responses
  const [resumeText, setResumeText] = useState("");
  const [skills, setSkills] = useState([]);
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState({});
  const [feedback, setFeedback] = useState(null);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  // Step 1: Send resume to backend to extract skills
  const analyzeResume = async () => {
    setError("");
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/analyze-resume`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ resume_text: resumeText }),
      });
      const data = await res.json();
      setSkills(data.skills || []);
    } catch (err) {
      setError("Failed to analyze resume.");
    }
    setLoading(false);
  };

  // Step 2: Generate interview questions based on detected skills
  const generateQuestions = async () => {
    setError("");
    setLoading(true);
    try {
      const res = await fetch(`${API_BASE}/generate-questions`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ skills }),
      });
      const data = await res.json();
      setQuestions(data.questions);
    } catch (err) {
      setError("Failed to generate questions.");
    }
    setLoading(false);
  };

  // Step 3: Submit user answers and receive AI-powered feedback
  const submitAnswers = async () => {
    setError("");
    setLoading(true);
    try {
      const qa_pairs = questions.map((q) => ({
        question: q.question,
        answer: answers[q.question] || "",
      }));

      const res = await fetch(`${API_BASE}/evaluate-answers`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ qa_pairs }),
      });

      const data = await res.json();
      setFeedback(data);
    } catch (err) {
      setError("Failed to evaluate answers.");
    }
    setLoading(false);
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

        {/* Section 1: Resume input */}
        <textarea
          placeholder="Paste your resume text here"
          value={resumeText}
          onChange={(e) => setResumeText(e.target.value)}
          rows={8}
        />

        <button onClick={analyzeResume} disabled={loading || !resumeText}>
          Extract Skills
        </button>

        {/* Section 2: Display extracted skills and prompt for questions */}
        {skills.length > 0 && (
          <>
            <h3>Your Skills</h3>
            <ul>
              {skills.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>
            <button onClick={generateQuestions} disabled={loading}>
              Generate Questions
            </button>
          </>
        )}

        {/* Section 3: Interview questions and user answers */}
        {questions.length > 0 && (
          <>
            <h3>Interview Questions</h3>
            {questions.map((q, i) => (
              <div key={i} className="question-block">
                <p><strong>{q.question}</strong></p>
                <textarea
                  rows={3}
                  placeholder="Type your answer here"
                  onChange={(e) =>
                    setAnswers({ ...answers, [q.question]: e.target.value })
                  }
                />
              </div>
            ))}
            <button onClick={submitAnswers} disabled={loading}>
              Get Feedback
            </button>
          </>
        )}

        {/* Loading and error states */}
        {loading && <p>Processing your request...</p>}
        {error && <p className="error">⚠️ {error}</p>}

        {/* Section 4: Feedback results and performance summary */}
        {feedback && (
          <>
            <h3>Your Interview Performance</h3>
            {feedback.evaluations.map((e, i) => (
              <div key={i} className="feedback-block">
                <p><strong>{e.question}</strong></p>
                <p><strong>Score:</strong> {e.score}/10</p>
                <p>{e.feedback}</p>
              </div>
            ))}

            <h4>What You Did Well</h4>
            <ul>
              {feedback.strengths.map((s, i) => (
                <li key={i}>{s}</li>
              ))}
            </ul>

            <h4>Areas to Focus On</h4>
            <ul>
              {feedback.improvements.map((i, idx) => (
                <li key={idx}>{i}</li>
              ))}
            </ul>

            <p><strong>Interview Readiness:</strong> {feedback.overall_readiness_summary}</p>
          </>
        )}
      </div>
    </div>
  );
}

export default App;
