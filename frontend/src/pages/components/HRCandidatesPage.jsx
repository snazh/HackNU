import { useState, useEffect } from "react";

function HRCandidatesPage() {
  const [candidates, setCandidates] = useState([]);
  const [selectedCandidate, setSelectedCandidate] = useState(null);
  const [filter, setFilter] = useState("");
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);

  // Запрос на бекенд для получения кандидатов
  useEffect(() => {
    const fetchCandidates = async () => {
      try {
        const res = await fetch("http://localhost:8000/api/candidates"); // URL бекенда
        if (!res.ok) throw new Error("Ошибка загрузки кандидатов");
        const data = await res.json();
        setCandidates(data);
      } catch (err) {
        setError("Ошибка соединения с сервером");
      } finally {
        setLoading(false);
      }
    };

    fetchCandidates();
  }, []);

  // Фильтруем кандидатов по релевантности и имени
  const filteredCandidates = candidates
    .filter(c => !filter || c.relevance >= filter)
    .filter(c => c.name.toLowerCase().includes(search.toLowerCase()));

  if (loading) return <p className="p-8 text-gray-600">Загрузка кандидатов...</p>;

  return (
    <div className="min-h-screen flex bg-gray-100 p-8 space-x-6">
      {/* Список кандидатов */}
      <div className="w-1/3 bg-white shadow-md rounded-2xl p-6 flex flex-col space-y-4">
        <h2 className="text-2xl font-bold mb-4">Кандидаты</h2>

        {/* Фильтры */}
        <div className="flex flex-col space-y-2 mb-4">
          <input
            type="text"
            placeholder="Поиск по имени"
            value={search}
            onChange={e => setSearch(e.target.value)}
            className="px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400"
          />
          <div className="flex items-center space-x-2">
            <label>Фильтр по релевантности: </label>
            <input
              type="number"
              min="0"
              max="100"
              value={filter}
              onChange={e => setFilter(Number(e.target.value))}
              className="w-16 px-2 py-1 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400"
            />
            %
          </div>
        </div>

        <div className="flex-1 overflow-y-auto space-y-2">
          {filteredCandidates.map(c => (
            <div
              key={c.id}
              onClick={() => setSelectedCandidate(c)}
              className="p-3 border border-gray-200 rounded-lg cursor-pointer hover:bg-gray-50 transition"
            >
              <h3 className="font-semibold">{c.name}</h3>
              <p className="text-gray-500 text-sm">Релевантность: {c.relevance}%</p>
            </div>
          ))}
        </div>
      </div>

      {/* Панель кандидата */}
      {selectedCandidate && (
        <div className="flex-1 bg-white shadow-md rounded-2xl p-6 flex flex-col">
          <div className="flex justify-between items-center mb-4">
            <h2 className="text-2xl font-bold">{selectedCandidate.name}</h2>
            <button
              onClick={() => setSelectedCandidate(null)}
              className="text-gray-500 hover:text-black"
            >
              Закрыть
            </button>
          </div>

          <p className="mb-2 text-gray-600">Город: {selectedCandidate.city}</p>
          <p className="mb-2 text-gray-600">Опыт: {selectedCandidate.experience}</p>
          <p className="mb-2 text-gray-600">Формат: {selectedCandidate.format}</p>
          <p className="mb-2 text-gray-600">Желаемая зарплата: {selectedCandidate.salary}</p>
          <p className="mb-4 text-gray-700 font-medium">
            Причины релевантности: {selectedCandidate.summary}
          </p>

          <div className="flex-1 flex flex-col border-t border-gray-200 pt-4 space-y-2 overflow-y-auto">
            <h3 className="font-semibold mb-2">Переписка с ботом:</h3>
            {selectedCandidate.chat.length === 0 && <p className="text-gray-400">Нет сообщений</p>}
            {selectedCandidate.chat.map((msg, idx) => (
              <div
                key={idx}
                className={`p-2 rounded-md max-w-xs ${
                  msg.fromUser ? "bg-gray-200 self-end" : "bg-indigo-100 self-start"
                }`}
              >
                {msg.text}
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
}

export default HRCandidatesPage