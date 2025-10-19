// import { useState, useEffect } from "react";

// function UserPage() {
//   const [vacancies, setVacancies] = useState([]);
//   const [chatOpen, setChatOpen] = useState(false);
//   const [messages, setMessages] = useState([]);
//   const [input, setInput] = useState("");
//   const [loading, setLoading] = useState(true);
//   const [error, setError] = useState("");
//   const [selectedJobId, setSelectedJobId] = useState(null);

//   // Получаем вакансии с бекенда
//   useEffect(() => {
//     const fetchVacancies = async () => {
//       try {
//         const res = await fetch("http://localhost:8000/api/vacancies"); // эндпоинт бекенда
//         if (!res.ok) throw new Error("Ошибка при получении вакансий");
//         const data = await res.json();
//         setVacancies(data.vacancies || []); 
//       } catch (err) {
//         setError(err.message);
//       } finally {
//         setLoading(false);
//       }
//     };
//     fetchVacancies();
//   }, []);

//   // Отправка сообщений в чат и получение ответа от ИИ
//   const handleSend = async () => {
//     if (!input.trim()) return;

//     // Добавляем сообщение юзера локально
//     setMessages(prev => [...prev, { text: input, fromUser: true }]);
//     const userMessage = input;
//     setInput("");

//     try {
//       const res = await fetch("http://localhost:8000/api/chatbot", {
//         method: "POST",
//         headers: { "Content-Type": "application/json" },
//         body: JSON.stringify({ userMessage, jobId: selectedJobId, userId: 1 }),
//       });
//       const data = await res.json();

//       // Ответ ИИ
//       setMessages(prev => [...prev, { text: data.botMessage, fromUser: false }]);
//     } catch (err) {
//       setMessages(prev => [...prev, { text: "Ошибка соединения с сервером", fromUser: false }]);
//     }
//   };

//   if (loading) return <p className="p-8">Загрузка вакансий...</p>;
//   if (error) return <p className="p-8 text-red-500">{error}</p>;

//   return (
//     <div className="min-h-screen flex bg-gray-100">
//       {/* Список вакансий */}
//       <div className="flex-1 p-8">
//         <h1 className="text-3xl font-bold mb-6">Вакансии</h1>
//         <div className="space-y-4">
//           {vacancies.map(vacancy => (
//             <div key={vacancy.id} className="bg-white p-6 rounded-xl shadow-md flex justify-between items-center">
//               <div>
//                 <h2 className="text-xl font-semibold">{vacancy.title}</h2>
//                 <p className="text-gray-500">{vacancy.company} • {vacancy.location}</p>
//                 <p className="text-gray-600 mt-1">{vacancy.description}</p>
//                 <p className="text-gray-500 mt-1">Зарплата: {vacancy.salary || "По договоренности"}</p>
//                 <p className="text-gray-500 mt-1">Требуемое образование: {vacancy.education}</p>
//               </div>

//               {/* Кнопка отклика */}
//               <button
//                 onClick={() => {
//                   setChatOpen(true);
//                   setSelectedJobId(vacancy.id);

//                   // Отправка отклика на бэк
//                   fetch("http://localhost:8000/api/apply", {
//                     method: "POST",
//                     headers: { "Content-Type": "application/json" },
//                     body: JSON.stringify({ jobId: vacancy.id, userId: 1 }),
//                   });

//                   // Инициализация чата
//                   setMessages([
//                     { text: "Привет! Я бот, давай обсудим твою кандидатуру.", fromUser: false }
//                   ]);
//                 }}
//                 className="px-4 py-2 bg-indigo-600 text-white rounded hover:bg-indigo-700 transition"
//               >
//                 Отклик
//               </button>
//             </div>
//           ))}
//         </div>
//       </div>

//       {/* Чат-виджет */}
//       <div className={`fixed top-0 right-0 h-full w-96 bg-white shadow-2xl transform transition-transform duration-300 flex flex-col ${chatOpen ? "translate-x-0" : "translate-x-full"}`}>
//         {/* Верхняя панель */}
//         <div className="flex justify-between items-center p-4 border-b border-gray-200 bg-gray-50">
//           <h2 className="font-bold text-lg">Чат с ботом</h2>
//           <button onClick={() => setChatOpen(false)} className="text-gray-400 hover:text-gray-700 transition">✕</button>
//         </div>

//         {/* Сообщения */}
//         <div className="flex-1 p-4 overflow-y-auto flex flex-col space-y-2 bg-gray-50">
//           {messages.length === 0 && (
//             <p className="text-gray-400 text-sm self-center mt-4">
//               Бот начнёт диалог после отклика.
//             </p>
//           )}
//           {messages.map((msg, idx) => (
//             <div key={idx} className={`p-3 rounded-lg max-w-[75%] break-words ${msg.fromUser ? "bg-gray-200 self-end text-gray-900" : "bg-indigo-600 text-white self-start"}`}>
//               {msg.text}
//             </div>
//           ))}
//         </div>

//         {/* Поле ввода */}
//         <div className="p-4 border-t border-gray-200 bg-gray-50 flex space-x-2">
//           <input
//             type="text"
//             placeholder="Напишите сообщение..."
//             value={input}
//             onChange={e => setInput(e.target.value)}
//             onKeyDown={e => { if (e.key === "Enter") handleSend(); }}
//             className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-indigo-400"
//           />
//           <button
//             onClick={handleSend}
//             className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
//           >
//             Отправить
//           </button>
//         </div>
//       </div>
//     </div>
//   );
// }

// export default UserPage;

import { useState, useEffect } from "react";

function UserPage() {
  const [vacancies, setVacancies] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [chatOpen, setChatOpen] = useState(false);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [currentQuestions, setCurrentQuestions] = useState([]);
  const [answeredQuestions, setAnsweredQuestions] = useState([]);
  const [currentVacancy, setCurrentVacancy] = useState(null);

  // Получаем вакансии с бекенда
  useEffect(() => {
    const fetchVacancies = async () => {
      try {
        const res = await fetch("http://localhost:8000/vacancies");
        if (!res.ok) throw new Error("Ошибка при получении вакансий");
        const data = await res.json();
        setVacancies(data.vacancies || data);
      } catch (err) {
        setError(err.message);
      } finally {
        setLoading(false);
      }
    };
    fetchVacancies();
  }, []);

  // Открытие чат-виджета и получение первых вопросов
  const handleApply = async (vacancy) => {
    setCurrentVacancy(vacancy);
    setChatOpen(true);
    setMessages([{ text: "Привет! Я бот, давай обсудим твою кандидатуру.", fromUser: false }]);

    try {
      const res = await fetch("http://localhost:8000/api/first-questions", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ vacancyId: vacancy.id, userId: 1 }),
      });
      if (!res.ok) throw new Error("Ошибка получения вопросов");
      const data = await res.json();
      setCurrentQuestions(data.questions || []);
    } catch (err) {
      setMessages(prev => [...prev, { text: "Не удалось получить вопросы с сервера", fromUser: false }]);
    }
  };

  // Отправка ответа на вопрос
  const handleSend = async () => {
    if (!input.trim() || currentQuestions.length === 0) return;

    const question = currentQuestions[0];
    setMessages([...messages, { text: input, fromUser: true }]);
    setAnsweredQuestions([...answeredQuestions, { question, answer: input }]);
    setInput("");

    const remainingQuestions = currentQuestions.slice(1);
    setCurrentQuestions(remainingQuestions);

    // Если вопросы закончились, отправляем все ответы на бек для анализа
    if (remainingQuestions.length === 0) {
      try {
        const res = await fetch("http://localhost:8000/api/analyze", {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({ vacancyId: currentVacancy.id, userId: 1, answers: [...answeredQuestions, { question, answer: input }] }),
        });
        const data = await res.json();
        setMessages(prev => [...prev, { text: data.analysis || "Анализ завершен", fromUser: false }]);
      } catch (err) {
        setMessages(prev => [...prev, { text: "Ошибка при анализе", fromUser: false }]);
      }
    } else {
      // показываем следующий вопрос
      setMessages(prev => [...prev, { text: remainingQuestions[0].text, fromUser: false }]);
    }
  };

  if (loading) return <p className="p-8">Загрузка вакансий...</p>;
  if (error) return <p className="p-8 text-red-500">{error}</p>;

  return (
    <div className="min-h-screen flex bg-gray-100">
      {/* Список вакансий */}
      <div className="flex-1 p-8 space-y-4">
        <h1 className="text-3xl font-bold mb-6">Вакансии</h1>
        {vacancies.map(v => (
          <div key={v.id} className="bg-white p-6 rounded-xl shadow-md flex justify-between items-center hover:scale-105 transform transition">
            <div>
              <h2 className="text-xl font-semibold">{v.title}</h2>
              <p className="text-gray-500">{v.company} • {v.location}</p>
              <p className="text-gray-600 mt-1">{v.description}</p>
              <p className="text-gray-500 mt-1">Зарплата: {v.salary || "По договоренности"}</p>
              <p className="text-gray-500 mt-1">Образование: {v.education}</p>
            </div>
            <button
              onClick={() => handleApply(v)}
              className="px-4 py-2 bg-indigo-600 text-white rounded-lg hover:bg-indigo-700 transition"
            >
              Отклик
            </button>
          </div>
        ))}
      </div>

      {/* Чат-виджет */}
      <div className={`fixed top-0 right-0 h-full w-96 bg-white shadow-xl transform transition-transform duration-300 ${chatOpen ? "translate-x-0" : "translate-x-full"}`}>
        <div className="flex flex-col h-full">
          <div className="flex justify-between items-center p-4 border-b border-gray-200 bg-indigo-50">
            <h2 className="font-bold text-lg text-indigo-900">Чат с ИИ</h2>
            <button onClick={() => setChatOpen(false)} className="text-gray-500 hover:text-black">Закрыть</button>
          </div>

          <div className="flex-1 p-4 overflow-y-auto space-y-2">
            {messages.map((msg, idx) => (
              <div key={idx} className={`p-2 rounded-md max-w-xs ${msg.fromUser ? "bg-gray-200 self-end" : "bg-indigo-100 self-start"}`}>
                {msg.text}
              </div>
            ))}
          </div>

          {currentQuestions.length > 0 && (
            <div className="p-4 border-t border-gray-200 flex space-x-2">
              <input
                type="text"
                placeholder={currentQuestions[0].text}
                value={input}
                onChange={e => setInput(e.target.value)}
                className="flex-1 px-3 py-2 border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400"
              />
              <button onClick={handleSend} className="px-4 py-2 bg-gray-800 text-white rounded-lg hover:bg-black transition">Отправить</button>
            </div>
          )}
        </div>
      </div>
    </div>
  );
}

export default UserPage;
