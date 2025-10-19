import { useState } from "react";
import { useNavigate } from "react-router-dom";

function LoginPage() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleLogin = async (e) => {
    e.preventDefault();
    setError("");

    if (!email || !password) {
      setError("Пожалуйста, заполните все поля");
      return;
    }

    setLoading(true);

    try {
      const response = await fetch("http://localhost:8000/api/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ email, password }),
      });
          const data = await response.json();

        alert(JSON.stringify(data, null, 2));




      if (response.ok) {
        localStorage.setItem("token", data.access_token); // если бекенд FastAPI возвращает access_token
        const role = data.user.role;

        if (role === "user") navigate("/user");
        else if (role === "hr") navigate("/hr");
        else navigate("/"); // по умолчанию
      } else {
        setError(data.detail || "Неверный логин или пароль");
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
        <h2 className="text-3xl font-bold text-center mb-8">Вход в систему</h2>

        <form onSubmit={handleLogin} className="flex flex-col space-y-6">
          <input
            type="email"
            placeholder="example@gmail.com"
            className="w-full py-3 px-4 text-lg border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400 placeholder-gray-400 transition"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
            required
          />

          <input
            type="password"
            placeholder="Введите пароль"
            className="w-full py-3 px-4 text-lg border border-gray-300 rounded-lg focus:outline-none focus:ring-2 focus:ring-gray-400 placeholder-gray-400 transition"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
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
            {loading ? "Загрузка..." : "Войти"}
          </button>

          <p className="text-center text-gray-500 text-sm mt-2">
            Нет аккаунта?{" "}
            <span
              onClick={() => navigate("/register")}
              className="text-gray-800 font-medium hover:underline cursor-pointer"
            >
              Зарегистрируйтесь
            </span>
          </p>
        </form>
      </div>
    </div>
  );
}

export default LoginPage;
