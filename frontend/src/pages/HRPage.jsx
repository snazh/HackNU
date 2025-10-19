import { useNavigate } from "react-router-dom";

function HRPage() {
  const navigate = useNavigate();

  return (
    <div className="min-h-screen flex flex-col items-center justify-center bg-gray-50">
      <h1 className="text-3xl font-bold mb-12">Панель HR</h1>

      <div className="flex flex-col md:flex-row gap-6">
        {/* Кандидаты */}
        <button
          onClick={() => navigate("/hr/candidates")}
          className="w-64 h-32 bg-white text-gray-800 text-xl font-medium rounded-xl shadow-sm 
                     border border-gray-200 hover:shadow-md hover:bg-gray-100 transition"
        >
          Кандидаты
        </button>

        {/* Создание вакансии */}
        <button
          onClick={() => navigate("/hr/create-vacancy")}
          className="w-64 h-32 bg-white text-gray-800 text-xl font-medium rounded-xl shadow-sm 
                     border border-gray-200 hover:shadow-md hover:bg-gray-100 transition"
        >
          Создать вакансию
        </button>
      </div>
    </div>
  );
}

export default HRPage