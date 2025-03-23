import { useState } from "react";
import Head from "next/head";
import DashboardLayout from "../../components/layout/DashboardLayout";

export default function OpenAIConfig() {
  const [apiKey, setApiKey] = useState("");
  const [status, setStatus] = useState("");

  const handleCheck = async () => {
    try {
      const res = await fetch("/api/config/openai/check", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ api_key: apiKey }),
      });
      const data = await res.json();
      setStatus(data.message || "Kết nối thành công!");
    } catch (err) {
      setStatus("Lỗi kết nối OpenAI");
    }
  };

  return (
    <DashboardLayout>
      <Head>
        <title>Cấu hình OpenAI</title>
      </Head>
      <div className="bg-white shadow rounded-xl p-6 max-w-xl">
        <h1 className="text-xl font-bold text-pink-600 mb-4">🔐 Cấu hình OpenAI API</h1>
        <input
          className="w-full p-2 border border-gray-300 rounded mb-4"
          placeholder="Nhập OpenAI API Key"
          value={apiKey}
          onChange={(e) => setApiKey(e.target.value)}
        />
        <button
          onClick={handleCheck}
          className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded"
        >
          Kiểm tra kết nối
        </button>
        {status && <p className="text-green-600 mt-2">{status}</p>}
      </div>
    </DashboardLayout>
  );
}
