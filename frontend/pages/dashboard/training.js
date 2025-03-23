// frontend/pages/dashboard/training.js
import { useState } from "react";
import Head from "next/head";
import DashboardLayout from "../../components/layout/DashboardLayout";

export default function TrainingUpload() {
  const [files, setFiles] = useState([]);
  const [status, setStatus] = useState("");
  const [uploadedFiles, setUploadedFiles] = useState([]);

  const handleUpload = async () => {
    if (!files.length) return setStatus("Chưa chọn file nào nhaaa 😢");

    const formData = new FormData();
    Array.from(files).forEach((file) => formData.append("files", file));

    try {
      const res = await fetch("/api/train/upload", {
        method: "POST",
        body: formData,
      });
      const data = await res.json();
      setStatus("📦 Upload thành công!");
      setUploadedFiles(data.files || []);
    } catch (err) {
      setStatus("❌ Lỗi khi upload file");
    }
  };

  const handleTrain = async () => {
    try {
      const res = await fetch("/api/train/start", { method: "POST" });
      const data = await res.json();
      setStatus(data.message || "✅ Đã bắt đầu train bot!");
    } catch (err) {
      setStatus("❌ Lỗi khi train dữ liệu");
    }
  };

  return (
    <DashboardLayout>
      <Head><title>Huấn luyện Bot</title></Head>
      <div className="bg-white shadow rounded-xl p-6 space-y-6 max-w-2xl">
        <h1 className="text-2xl font-bold text-pink-600 mb-4">📚 Tải tài liệu huấn luyện</h1>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Chọn file huấn luyện (.pdf, .txt)</label>
          <input
            type="file"
            multiple
            accept=".pdf,.txt"
            onChange={(e) => setFiles(e.target.files)}
            className="w-full"
          />
        </div>

        <button onClick={handleUpload} className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded">
          Upload file
        </button>

        <div>
          <h2 className="text-sm font-medium text-gray-700 mb-1">📄 File đã upload:</h2>
          <ul className="list-disc ml-5 text-sm text-gray-600">
            {uploadedFiles.map((f, i) => <li key={i}>{f}</li>)}
          </ul>
        </div>

        <button onClick={handleTrain} className="bg-green-500 hover:bg-green-600 text-white px-4 py-2 rounded">
          Bắt đầu train bot
        </button>

        {status && <p className="text-sm text-pink-600 mt-2">{status}</p>}
      </div>
    </DashboardLayout>
  );
}
