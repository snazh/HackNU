import {useState, useEffect} from "react"

function ChatWidget({ openOnInit = false, systemMessage = "" }) {
  const [chatOpen, setChatOpen] = useState(openOnInit);
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");

  useEffect(() => {
    if (openOnInit && systemMessage) {
      setMessages([{ text: systemMessage, fromUser: false }]);
    }
  }, [openOnInit, systemMessage]);

  const handleSend = () => {
    if (!input.trim()) return;
    const newMsg = { text: input, fromUser: true };
    setMessages(prev => [...prev, newMsg]);
    setInput("");

    fetch("http://localhost:5000/api/bot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: input, userId: 1, jobId: 2 }),
    })
      .then(res => res.json())
      .then(data => setMessages(prev => [...prev, { text: data.reply, fromUser: false }]));
  };

  return (
    <div className={`fixed top-0 right-0 h-full w-80 bg-white shadow-xl transition-transform duration-300 ${chatOpen ? "translate-x-0" : "translate-x-full"}`}>
      {/* header, messages и input как в нашем виджете */}
    </div>
  );
}

// инициализация виджета
export function initChatWidget({ containerId, openOnInit, systemMessage }) {
  const container = document.getElementById(containerId);
  ReactDOM.render(<ChatWidget openOnInit={openOnInit} systemMessage={systemMessage} />, container);
}