// frontend/pages/dashboard/logs.js
import { useEffect, useState } from "react";
import DashboardLayout from "../../components/layout/DashboardLayout";
import Head from "next/head";

export default function LogsPage() {
  const [logs, setLogs] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchLogs = async () => {
      try {
        const res = await fetch("/api/logs");
        const data = await res.json();
        setLogs(data.logs || []);
      } catch {
        // fallback demo
        setLogs([
          {
            user: "Nguyễn Văn A",
            question: "Học phí ngành Tài chính là bao nhiêu vậy?",
            response: "Học phí 18 triệu/năm nha bạn yêu ơi 😘",
            time: "2025-03-23 10:12:45",
          },
          {
            user: "Trần Thị B",
            question: "Em cần tư vấn chọn ngành phù hợp ạ!",
            response: "Oanh Bihi sẽ giúp bạn, cho mình xin sở thích & điểm mạnh nhé 💖",
            time: "2025-03-23 10:15:01",
          },
        ]);
      } finally {
        setLoading(false);
      }
    };

    fetchLogs();
  }, []);

  return (
    <DashboardLayout>
      <Head><title>Nhật ký hội thoại</title></Head>
      <div className="bg-white shadow rounded-xl p-6">
        <h1 className="text-2xl font-bold text-pink-600 mb-4">📜 Nhật ký hội thoại</h1>
        {loading ? (
          <p>⏳ Đang tải dữ liệu...</p>
        ) : (
          <div className="overflow-x-auto">
            <table className="min-w-full text-sm text-left">
              <thead className="bg-pink-100 text-pink-700">
                <tr>
                  <th className="px-4 py-2">🕒 Thời gian</th>
                  <th className="px-4 py-2">👤 Người dùng</th>
                  <th className="px-4 py-2">❓ Câu hỏi</th>
                  <th className="px-4 py-2">💬 Phản hồi</th>
                </tr>
              </thead>
              <tbody>
                {logs.map((log, i) => (
                  <tr key={i} className="border-b hover:bg-pink-50">
                    <td className="px-4 py-2 text-gray-500">{log.time}</td>
                    <td className="px-4 py-2 font-medium">{log.user}</td>
                    <td className="px-4 py-2">{log.question}</td>
                    <td className="px-4 py-2 text-pink-700">{log.response}</td>
                  </tr>
                ))}
              </tbody>
            </table>
          </div>
        )}
      </div>
    </DashboardLayout>
  );
}
