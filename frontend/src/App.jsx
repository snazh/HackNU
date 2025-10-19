import { Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage";
import HRPage from "./pages/HRPage"
import UserPage from "./pages/UserPage"
import HRCandidatesPage from "./pages/components/HRCandidatesPage"
import HRCreatorPage from "./pages/components/HRCreatorPage"
import './App.css'

function App() {
  return(
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/hr" element={<HRPage />} />
        <Route path="/hr/candidates" element={<HRCandidatesPage />}/>
        <Route path="/hr/create-vacancy" element={<HRCreatorPage />}/>
        <Route path="/user" element={<UserPage />} />
      </Routes>
  );
}

export default App
