import { useState, useEffect } from "react";

function UserPage() {
  const [vacancies, setVacancies] = useState([]);
  const [chatOpen, setChatOpen] = useState(false);
  const [finalResult, setFinalResult] = useState(null);
  const [selectedVacancy, setSelectedVacancy] = useState(null);

  useEffect(() => {
    fetch("http://localhost:8000/api/vacancies", { credentials: "include" })
      .then(res => res.json())
      .then(data => setVacancies(data.data || []))
      .catch(console.error);
  }, []);

  const handleApply = async (vacancy) => {
    setChatOpen(true);
    setSelectedVacancy(vacancy);
    setFinalResult(null);

    try {
      const res = await fetch(`http://localhost:8000/api/vacancies/${vacancy.id}/apply`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
      });

      const data = await res.json();

      if (data?.data) {
        let parsed;
        try {
          const cleaned = data.data.replace(/```json|```/g, "").trim();
          parsed = JSON.parse(cleaned);
        } catch {
          parsed = null;
        }

        if (parsed) setFinalResult(parsed);
      }
    } catch {
      setFinalResult({ error: "Connection error with the server" });
    }
  };

  return (
    <div className="min-h-screen flex bg-gray-100">
      {/* Vacancy list */}
      <div className="flex-1 p-10">
        <h1 className="text-4xl font-bold mb-8">Vacancies</h1>
        <div className="grid grid-cols-1 xl:grid-cols-2 gap-8">
          {vacancies.map(v => (
            <div
              key={v.id}
              className="bg-white p-8 rounded-2xl shadow-lg hover:shadow-xl transition duration-300"
            >
              <div className="flex justify-between items-start mb-4">
                <div>
                  <h2 className="text-2xl font-semibold text-gray-900">{v.title}</h2>
                  <p className="text-gray-500 text-sm mt-1">
                    {v.company} • {v.location}
                  </p>
                </div>
                <span className="px-3 py-1 bg-indigo-100 text-indigo-700 rounded-full text-sm font-medium">
                  {v.employment_form || "Full-time"}
                </span>
              </div>

              <div className="space-y-2 text-gray-700 mb-6">
                {v.salary && (
                  <p>
                    💰 <span className="font-medium">Salary:</span> {v.salary}
                  </p>
                )}
                {v.education_level && (
                  <p>
                    🎓 <span className="font-medium">Education:</span> {v.education_level}
                  </p>
                )}
                {v.skills && (
                  <p>
                    🧠 <span className="font-medium">Skills:</span> {v.skills.join(", ")}
                  </p>
                )}
                {v.description && (
                  <p className="text-gray-600 line-clamp-3">{v.description}</p>
                )}
              </div>

              <button
                onClick={() => handleApply(v)}
                className="w-full py-3 bg-indigo-600 text-white rounded-xl hover:bg-indigo-700 transition font-semibold"
              >
                Apply
              </button>
            </div>
          ))}
        </div>
      </div>

      {/* Result widget */}
      <div
        className={`fixed top-0 right-0 h-full w-[420px] bg-white shadow-2xl transform transition-transform duration-300 ${
          chatOpen ? "translate-x-0" : "translate-x-full"
        }`}
      >
        <div className="flex flex-col h-full">
          <div className="flex justify-between items-center p-5 border-b border-gray-200">
            <h2 className="font-bold text-lg">
              {selectedVacancy ? selectedVacancy.title : "Analysis result"}
            </h2>
            <button onClick={() => setChatOpen(false)} className="text-gray-500 hover:text-black">
              ✕
            </button>
          </div>

          <div className="flex-1 p-6 overflow-y-auto">
            {finalResult ? (
              finalResult.error ? (
                <p className="text-red-500 text-center">{finalResult.error}</p>
              ) : (
                <div className="bg-indigo-50 border border-indigo-200 rounded-xl p-5 shadow-sm">
                  <p className="text-2xl font-semibold text-indigo-700 mb-3">
                    🎯 Match: {finalResult.final_relevance_percentage}%
                  </p>
                  <p className="text-gray-800 leading-relaxed">
                    {finalResult.final_summary_for_employer}
                  </p>
                </div>
              )
            ) : (
              <p className="text-gray-500 text-center mt-10">
                The analysis will appear after applying
              </p>
            )}
          </div>
        </div>
      </div>
    </div>
  );
}

export default UserPage;
