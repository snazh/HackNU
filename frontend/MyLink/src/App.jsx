import { Routes, Route } from "react-router-dom";
import LoginPage from "./pages/LoginPage"
import RegisterPage from "./pages/RegisterPage";
import HRPage from "./pages/HRPage"
import UserPage from "./pages/UserPage"
import './App.css'

function App() {
  return(
      <Routes>
        <Route path="/" element={<LoginPage />} />
        <Route path="/register" element={<RegisterPage />} />
        <Route path="/hr" element={<HRPage />} />
        <Route path="/user" element={<UserPage />} />
      </Routes>
  );
}

export default App
