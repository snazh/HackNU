import { useState } from "react";

function HRCreatorPage() {
  const [title, setTitle] = useState("");
  const [description, setDescription] = useState("");
  const [company, setCompany] = useState("");
  const [location, setLocation] = useState("");
  const [salary, setSalary] = useState("");
  const [status, setStatus] = useState("open");
  const [education, setEducation] = useState("any");
  const [skills, setSkills] = useState([]);
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  const educationOptions = [
    { value: "high_school", label: "Среднее" },
    { value: "bachelor", label: "Бакалавр" },
    { value: "master", label: "Магистр" },
    { value: "phd", label: "Докторантура" },
    { value: "any", label: "Любое" },
  ];

  const statusOptions = [
    { value: "open", label: "Открыта" },
    { value: "closed", label: "Закрыта" },
    { value: "paused", label: "Приостановлена" },
  ];

  const handleSubmit = async (e) => {
    e.preventDefault();
    setError("");

    const vacancyData = {
      title,
      description,
      company,
      location,
      salary,
      status,
      education,
      skills,
    };

    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/vacancies/", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(vacancyData),
      });

      const data = await response.json();

      if (response.ok) {
        alert("Вакансия создана успешно!");
        // Очистить форму
        setTitle("");
        setDescription("");
        setCompany("");
        setLocation("");
        setSalary("");
        setStatus("open");
        setEducation("any");
        setSkills([]);
      } else {
        setError(data.detail || "Ошибка при создании вакансии");
      }
    } catch (err) {
      setError("Ошибка соединения с сервером");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex justify-center items-start bg-gray-50 p-8">
      <div className="bg-white p-8 rounded-xl shadow-md w-full max-w-2xl">
        <h1 className="text-2xl font-bold mb-6">Создание вакансии</h1>

        <form className="flex flex-col space-y-4" onSubmit={handleSubmit}>
          <input
            type="text"
            placeholder="Название вакансии"
            value={title}
            onChange={(e) => setTitle(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400"
            required
          />

          <textarea
            placeholder="Описание вакансии"
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400"
            rows={4}
            required
          />

          <input
            type="text"
            placeholder="Компания"
            value={company}
            onChange={(e) => setCompany(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400"
            required
          />

          <input
            type="text"
            placeholder="Город/Локация"
            value={location}
            onChange={(e) => setLocation(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400"
          />

          <input
            type="text"
            placeholder="Зарплата"
            value={salary}
            onChange={(e) => setSalary(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400"
          />

          {/* Статус вакансии */}
          <select
            value={status}
            
            onChange={(e) => setStatus(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400"
          >
            <option value="" disabled>Статус вакансии</option>
            {statusOptions.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>

          {/* Уровень образования */}
          <select
            value={education}
            onChange={(e) => setEducation(e.target.value)}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400"
          >
            <option value="" disabled>Уровень образования</option>
            {educationOptions.map(opt => (
              <option key={opt.value} value={opt.value}>{opt.label}</option>
            ))}
          </select>

          {/* Список навыков */}
          <input
            type="text"
            placeholder="Навыки (через запятую)"
            value={skills.join(", ")}
            onChange={(e) => setSkills(e.target.value.split(",").map(s => s.trim()))}
            className="px-4 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400"
          />

          {error && <p className="text-red-500">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className={`py-3 rounded-lg text-white font-medium transition ${
              loading ? "bg-gray-400 cursor-not-allowed" : "bg-indigo-600 hover:bg-indigo-700"
            }`}
          >
            {loading ? "Создание..." : "Создать вакансию"}
          </button>
        </form>
      </div>
    </div>
  );
}

export default HRCreatorPage