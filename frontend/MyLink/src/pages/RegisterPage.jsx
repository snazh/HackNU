// RegisterPage.jsx
import { useState } from "react";
import { useNavigate } from "react-router-dom";

function RegisterPage() {
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleRegister = async (e) => {
    e.preventDefault();
    setError("");

    if (!name || !email || !password) {
      setError("Пожалуйста, заполните все поля");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://localhost:5000/register", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ name, email, password }),
      });

      const data = await response.json();

      if (data.status === "ok") {
        navigate("/"); // редирект на логин
      } else {
        setError(data.message || "Ошибка регистрации");
      }
    } catch (err) {
      setError("Ошибка соединения с сервером");
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-gray-100">
      <div className="bg-white text-gray-900 rounded-2xl shadow-md p-10 w-[400px]">
        <h2 className="text-3xl font-bold text-center mb-8">Регистрация</h2>

        <form onSubmit={handleRegister} className="flex flex-col space-y-6">
          <input
            type="text"
            placeholder="Имя"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full py-3 px-4 text-lg border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400 placeholder-gray-400 transition"
            required
          />

          <input
            type="email"
            placeholder="example@gmail.com"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            className="w-full py-3 px-4 text-lg border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400 placeholder-gray-400 transition"
            required
          />

          <input
            type="password"
            placeholder="Введите пароль"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            className="w-full py-3 px-4 text-lg border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400 placeholder-gray-400 transition"
            required
          />

          {error && <p className="text-red-500 text-center text-sm">{error}</p>}

          <button
            type="submit"
            disabled={loading}
            className={`w-full py-3 rounded-lg text-white font-semibold transition ${
              loading ? "bg-gray-400 cursor-not-allowed" : "bg-gray-800 hover:bg-black"
            }`}
          >
            {loading ? "Загрузка..." : "Зарегистрироваться"}
          </button>

          <p className="text-center text-gray-500 text-sm mt-2">
            Уже есть аккаунт?{" "}
            <span
              onClick={() => navigate("/")}
              className="text-gray-800 font-medium hover:underline cursor-pointer"
            >
              Войти
            </span>
          </p>
        </form>
      </div>
    </div>
  );
}

export default RegisterPage