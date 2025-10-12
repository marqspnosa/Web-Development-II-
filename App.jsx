import { useState } from 'react'
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import axios from 'axios'

function App() {
  const [count, setCount] = useState(0)
  // State to hold the HTML content from the FastAPI backend
  const [htmlContent, setHtmlContent] = useState(null)

  const fastapiExample = async () => {
    console.log("We are trying to reach out to FastAPI")
    try {
      const response = await axios.get("http://localhost:8000/react-demo")
      console.log(JSON.stringify(response.data));
      // Store the received HTML string in the state
      setHtmlContent(response.data);
    } catch (error) {
      console.error("Error fetching data:", error);
      setHtmlContent("<p style='color:red;'>Failed to fetch data.</p>");
    }
  }

  return (
    <>
      <div>
        <a href="https://vite.dev" target="_blank">
          <img src={viteLogo} className="logo" alt="Vite logo" />
        </a>
        <a href="https://react.dev" target="_blank">
          <img src={reactLogo} className="logo react" alt="React logo" />
        </a>
      </div>
      <h1>Vite + React</h1>
      <div className="card">
        <button onClick={() => setCount((count) => count + 1)}>
          count is {count}
        </button>
        <p>
          Edit <code>src/App.jsx</code> and save to test HMR
        </p>
      </div>

      <div className="card">
        <button onClick={fastapiExample}>
          Call FastAPI and display HTML
        </button>
        {/* Conditional rendering: only show the HTML if it exists in the state */}
        {htmlContent && (
          <div dangerouslySetInnerHTML={{ __html: JSON.stringify(htmlContent) }} />
        )}
      </div>

      <p className="read-the-docs">
        Click on the Vite and React logos to learn more
      </p>
    </>
  )
}

export default App