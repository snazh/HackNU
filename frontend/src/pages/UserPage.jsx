import { useState, useEffect } from "react";

function UserPage() {
  const [vacancies, setVacancies] = useState([]);
  const [chatOpen, setChatOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [questions, setQuestions] = useState([]);
  const [answers, setAnswers] = useState([]);
  const [currentQuestionIndex, setCurrentQuestionIndex] = useState(0);
  const [currentVacancyId, setCurrentVacancyId] = useState(null);

  // Загружаем вакансии
  useEffect(() => {
    fetch("http://localhost:8000/api/vacancies", {
      credentials: "include" // cookies для авторизации
    })
      .then(res => res.json())
      .then(data => setVacancies(data.data || []))
      .catch(err => console.error(err));
  }, []);

  const handleApply = async (vacancyId) => {
    setChatOpen(true);
    setCurrentVacancyId(vacancyId);

    try {
      const res = await fetch(`http://localhost:8000/api/vacancies/${vacancyId}/apply`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        credentials: "include",
        body: JSON.stringify({}) // user_id сервер берёт из cookies
      });
      const data = await res.json();
      if (data.status === "Success") {
        setQuestions(data.data);
        setMessages([{ text: data.data[0], fromUser: false }]);
        setCurrentQuestionIndex(0);
        setAnswers([]);
      }
    } catch (err) {
      console.error(err);
    }
  };

  const handleSend = () => {
    if (!input.trim()) return;

    const newAnswers = [...answers, input];
    setAnswers(newAnswers);
    setMessages(prev => [...prev, { text: input, fromUser: true }]);
    setInput("");

    const nextIndex = currentQuestionIndex + 1;
    if (nextIndex < questions.length) {
      setMessages(prev => [...prev, { text: questions[nextIndex], fromUser: false }]);
      setCurrentQuestionIndex(nextIndex);
    } else {
      alert("Ваши ответы:\n" + newAnswers.map((a, i) => `${i + 1}. ${a}`).join("\n"));
      // сбрасываем чат
      setChatOpen(false);
      setMessages([]);
      setQuestions([]);
      setAnswers([]);
      setCurrentQuestionIndex(0);
      setCurrentVacancyId(null);
    }
  };

  return (
    <div className="min-h-screen flex bg-gray-100">
      <div className="flex-1 p-8">
        <h1 className="text-3xl font-bold mb-6">Вакансии</h1>
        <div className="space-y-4">
          {vacancies.map(v => (
            <div key={v.id} className="bg-white p-6 rounded-xl shadow-md flex justify-between items-center">
              <div>
                <h2 className="text-xl font-semibold">{v.title}</h2>
                <p className="text-gray-500">{v.company} • {v.location}</p>
              </div>
              <button
                onClick={() => handleApply(v.id)}
                className="px-4 py-2 bg-indigo-600 text-white rounded"
              >
                Отклик
              </button>
            </div>
          ))}
        </div>
      </div>

      <div className={`fixed top-0 right-0 h-full w-80 bg-white shadow-xl transform transition-transform duration-300 ${chatOpen ? "translate-x-0" : "translate-x-full"}`}>
        <div className="flex flex-col h-full">
          <div className="flex justify-between items-center p-4 border-b border-gray-200">
            <h2 className="font-bold text-lg">Чат с ботом</h2>
            <button onClick={() => setChatOpen(false)} className="text-gray-500 hover:text-black">Закрыть</button>
          </div>

          <div className="flex-1 p-4 overflow-y-auto space-y-2">
            {messages.map((msg, idx) => (
              <div key={idx} className={`p-2 rounded-md ${msg.fromUser ? "bg-gray-200 self-end" : "bg-indigo-100 self-start"} max-w-xs`}>
                {msg.text}
              </div>
            ))}
          </div>

          {questions.length > 0 && (
            <div className="p-4 border-t border-gray-200 flex space-x-2">
              <input
                type="text"
                placeholder="Напишите сообщение..."
                value={input}
                onChange={e => setInput(e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400"
              />
              <button
                onClick={handleSend}
                className="px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-black transition"
              >
                Отправить
              </button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default UserPage;
