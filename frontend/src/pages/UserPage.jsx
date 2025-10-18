import { useState } from "react";

const dummyVacancies = [
  { id: 1, title: "Frontend-разработчик", company: "TechCorp", location: "Алматы" },
  { id: 2, title: "HR-специалист", company: "BizGroup", location: "Нур-Султан" },
  { id: 3, title: "Data Analyst", company: "DataLab", location: "Шымкент" },
];

function UserPage() {
  const [chatOpen, setChatOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  const handleSend = () => {
    if (!input.trim()) return;
    setMessages([...messages, { text: input, fromUser: true }]);
    setInput("");

    // Имитируем ответ чат-бота
    setTimeout(() => {
      setMessages(prev => [...prev, { text: "Спасибо за отклик! Мы свяжемся с вами.", fromUser: false }]);
    }, 1000);
  };

  return (
    <div className="min-h-screen flex bg-gray-100">
      {/* Список вакансий */}
      <div className="flex-1 p-8">
        <h1 className="text-3xl font-bold mb-6">Вакансии</h1>
        <div className="space-y-4">
          {dummyVacancies.map(vacancy => (
            <div key={vacancy.id} className="bg-white p-6 rounded-xl shadow-md flex justify-between items-center">
              <div>
                <h2 className="text-xl font-semibold">{vacancy.title}</h2>
                <p className="text-gray-500">{vacancy.company} • {vacancy.location}</p>
              </div>
              <button
                    onClick={() =>  {
                    setChatOpen(true);
                    fetch("http://localhost:5000/api/apply", {
                    method: "POST",
                    headers: { "Content-Type": "application/json" },
                    body: JSON.stringify({ jobId: job.id, userId: 1 }),
                    });
              initChatWidget({
                containerId: "chat-widget",
                openOnInit: true,
                systemMessage: "Привет! Я бот, давай обсудим твою кандидатуру."
              });
            }}
            className="px-4 py-2 bg-indigo-600 text-white rounded"
          >
            Отклик
          </button>
            </div>
          ))}
        </div>
      </div>

      {/* Чат-виджет */}
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
        </div>
      </div>
    </div>
  );
}

export default UserPage;