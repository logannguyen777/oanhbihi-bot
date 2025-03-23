// frontend/pages/dashboard/conversations.js
import { useEffect, useState } from "react";
import Head from "next/head";
import DashboardLayout from "../../components/layout/DashboardLayout";
import { io } from "socket.io-client";

const socket = io("http://localhost:8000"); // ✅ Đảm bảo backend chạy cùng domain/port

export default function ConversationsPage() {
  const [users, setUsers] = useState([]);
  const [replyBox, setReplyBox] = useState({});
  const [loading, setLoading] = useState(true);

  const fetchUsers = async () => {
    const res = await fetch("/api/admin/conversations");
    const data = await res.json();
    setUsers(data.users || []);
    setLoading(false);
  };

  useEffect(() => {
    fetchUsers();
    socket.on("chat_update", () => {
      fetchUsers();
    });
    return () => socket.disconnect();
  }, []);

  const toggleBot = async (id) => {
    await fetch("/api/admin/toggle-bot", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: id }),
    });
  };

  const handleReply = async (id) => {
    await fetch("/api/admin/reply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: id, message: replyBox[id] }),
    });
    setReplyBox((prev) => ({ ...prev, [id]: "" }));
  };

  return (
    <DashboardLayout>
      <Head><title>Quản lý hội thoại</title></Head>
      <div className="bg-white shadow rounded-xl p-6">
        <h1 className="text-2xl font-bold text-pink-600 mb-4">📞 Quản lý hội thoại</h1>

        {loading ? (
          <p>Đang tải...</p>
        ) : (
          <table className="min-w-full text-sm">
            <thead className="bg-pink-100 text-pink-700">
              <tr>
                <th className="px-4 py-2">👤 Người dùng</th>
                <th className="px-4 py-2">📱 Kênh</th>
                <th className="px-4 py-2">📨 Tin nhắn gần nhất</th>
                <th className="px-4 py-2">🤖 Bot</th>
                <th className="px-4 py-2">✍️ Trả lời</th>
              </tr>
            </thead>
            <tbody>
              {users.map((u) => (
                <tr key={u.id} className="border-b">
                  <td className="px-4 py-2 font-medium">{u.name}</td>
                  <td className="px-4 py-2">{u.channel}</td>
                  <td className="px-4 py-2 text-gray-600">{u.lastMessage}</td>
                  <td className="px-4 py-2">
                    <button
                      onClick={() => toggleBot(u.id)}
                      className={`px-3 py-1 rounded text-white text-sm ${
                        u.botEnabled ? "bg-green-500" : "bg-gray-400"
                      }`}
                    >
                      {u.botEnabled ? "Bật" : "Tắt"}
                    </button>
                  </td>
                  <td className="px-4 py-2">
                    <div className="flex gap-2">
                      <input
                        value={replyBox[u.id] || ""}
                        onChange={(e) =>
                          setReplyBox((prev) => ({ ...prev, [u.id]: e.target.value }))
                        }
                        className="border px-2 py-1 rounded text-sm"
                        placeholder="Nhập phản hồi"
                      />
                      <button
                        onClick={() => handleReply(u.id)}
                        className="bg-pink-500 hover:bg-pink-600 text-white px-3 py-1 rounded text-sm"
                      >
                        Gửi
                      </button>
                    </div>
                  </td>
                </tr>
              ))}
            </tbody>
          </table>
        )}
      </div>
    </DashboardLayout>
  );
}
