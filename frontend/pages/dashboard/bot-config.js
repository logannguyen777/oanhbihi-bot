// frontend/pages/dashboard/bot-config.js
import { useState } from "react";
import Head from "next/head";
import DashboardLayout from "../../components/layout/DashboardLayout";

export default function BotConfig() {
  const [form, setForm] = useState({
    name: "",
    age: "",
    gender: "",
    tone: "",
    greeting: "",
    style: "",
  });
  const [status, setStatus] = useState("");

  const handleChange = (e) => {
    setForm({ ...form, [e.target.name]: e.target.value });
  };

  const handleSave = async () => {
    const res = await fetch("/api/config/persona", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(form),
    });
    const data = await res.json();
    setStatus(data.message || "Đã lưu!");
  };

  return (
    <DashboardLayout>
      <Head><title>Bot & Persona</title></Head>
      <div className="bg-white shadow rounded-xl p-6 max-w-xl space-y-4">
        <h1 className="text-xl font-bold text-pink-600">👩‍🎤 Cấu hình Bot & Persona</h1>
        {Object.entries(form).map(([key, value]) => (
          <input
            key={key}
            name={key}
            placeholder={key}
            value={value}
            onChange={handleChange}
            className="w-full p-2 border rounded"
          />
        ))}
        <button
          onClick={handleSave}
          className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded"
        >
          Lưu cấu hình
        </button>
        {status && <p className="text-green-600 text-sm">{status}</p>}
      </div>
    </DashboardLayout>
  );
}
