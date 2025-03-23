import { useEffect, useState } from "react";
import Layout from "@/components/Layout";
import AuthGuard from "@/components/AuthGuard";

export default function AdminChatLog() {
  const [conversations, setConversations] = useState([]);
  const [selected, setSelected] = useState(null);
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/admin_chat`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => res.json())
      .then((data) => setConversations(data || []));
  }, []);

  const handleSelect = async (conv) => {
    setLoading(true);
    const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/admin_chat/${conv.session_id}`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    });
    const detail = await res.json();
    setSelected(detail);
    setLoading(false);
  };

  return (
    <AuthGuard>
      <Layout>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
          <div className="bg-white p-4 rounded-xl shadow">
            <h2 className="font-bold text-lg mb-2">📋 Danh sách hội thoại</h2>
            <ul className="space-y-2 max-h-[70vh] overflow-auto">
              {conversations.map((conv, idx) => (
                <li
                  key={idx}
                  className={`p-3 rounded-lg cursor-pointer hover:bg-purple-100 ${
                    selected?.session_id === conv.session_id ? "bg-purple-200" : ""
                  }`}
                  onClick={() => handleSelect(conv)}
                >
                  <div className="font-semibold">🧑 {conv.user_name || "Người dùng ẩn danh"}</div>
                  <div className="text-sm text-gray-500">🕒 {new Date(conv.created_at).toLocaleString()}</div>
                </li>
              ))}
            </ul>
          </div>

          <div className="col-span-2 bg-white p-4 rounded-xl shadow">
            <h2 className="font-bold text-lg mb-4">🗂️ Chi tiết hội thoại</h2>
            {loading && <p>Đang tải nội dung...</p>}
            {!loading && selected && selected.messages && (
              <div className="space-y-3 max-h-[70vh] overflow-auto">
                {selected.messages.map((msg, i) => (
                  <div
                    key={i}
                    className={`chat ${msg.role === "user" ? "chat-end" : "chat-start"}`}
                  >
                    <div className="chat-image avatar">
                      <div className="w-8 rounded-full">
                        <img
                          src={msg.role === "user" ? "/user.png" : "/logo.png"}
                          alt="avatar"
                        />
                      </div>
                    </div>
                    <div
                      className={`chat-bubble ${
                        msg.role === "user" ? "chat-bubble-info" : "chat-bubble-primary"
                      }`}
                    >
                      {msg.content}
                    </div>
                  </div>
                ))}
              </div>
            )}
            {!loading && !selected && (
              <p className="text-gray-500">Hãy chọn một cuộc hội thoại để xem chi tiết nhé~</p>
            )}
          </div>
        </div>
      </Layout>
    </AuthGuard>
  );
}
