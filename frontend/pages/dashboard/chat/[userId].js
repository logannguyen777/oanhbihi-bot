// frontend/pages/dashboard/chat/[userId].js
import { useRouter } from "next/router";
import useSWR from "swr";
import { useState } from "react";
import DashboardLayout from "../../../components/layout/DashboardLayout";

const fetcher = (url) => fetch(url).then((r) => r.json());

export default function ChatDetailPage() {
  const router = useRouter();
  const { userId } = router.query;
  const { data, mutate } = useSWR(
    userId ? `/api/admin/conversations/${userId}` : null,
    fetcher
  );
  const [message, setMessage] = useState("");

  const handleSend = async () => {
    if (!message) return;
    await fetch("/api/admin/reply", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ user_id: userId, message }),
    });
    setMessage("");
    mutate();
  };

  return (
    <DashboardLayout>
      <div className="p-6 max-w-3xl mx-auto">
        <h1 className="text-xl font-bold text-pink-600 mb-4">💬 Hội thoại với User #{userId}</h1>

        <div className="bg-white shadow p-4 rounded h-[60vh] overflow-y-auto space-y-3">
          {data?.conversation?.map((msg) => (
            <div
              key={msg.id}
              className={`max-w-[75%] p-2 rounded ${
                msg.role === "admin"
                  ? "bg-pink-100 self-end ml-auto"
                  : "bg-gray-100"
              }`}
            >
              <p className="text-sm">{msg.message}</p>
              <p className="text-xs text-gray-400 mt-1">{msg.timestamp}</p>
            </div>
          ))}
        </div>

        <div className="flex gap-2 mt-4">
          <input
            value={message}
            onChange={(e) => setMessage(e.target.value)}
            className="w-full border px-3 py-2 rounded"
            placeholder="Nhập tin nhắn"
          />
          <button
            onClick={handleSend}
            className="bg-pink-500 text-white px-4 py-2 rounded"
          >
            Gửi
          </button>
        </div>
      </div>
    </DashboardLayout>
  );
}
