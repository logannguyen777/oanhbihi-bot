import { useState } from "react";
import Layout from "@/components/Layout";
import { apiFetch } from "@/hooks/useApi";
import Image from "next/image";

export default function ChatPage() {
  const [input, setInput] = useState("");
  const [messages, setMessages] = useState([]);
  const [loading, setLoading] = useState(false);

  const sendMessage = async () => {
    if (!input.trim()) return;
    const userMsg = { sender: "user", text: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setLoading(true);

    try {
      const res = await apiFetch("/chat", "POST", { input_text: input });
      const botMsg = { sender: "bot", text: res.response || "(Không có phản hồi 🤖)" };
      setMessages((prev) => [...prev, botMsg]);
    } catch (err) {
      const errMsg = { sender: "bot", text: "⚠️ Lỗi khi gọi bot: " + err.message };
      setMessages((prev) => [...prev, errMsg]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <Layout>
      <div className="max-w-3xl mx-auto px-4 py-6">
        <h2 className="text-2xl font-bold text-purple-700 mb-4">🎀 Trò chuyện với Oanh Bihi</h2>

        <div className="bg-white shadow rounded p-4 h-[60vh] overflow-y-auto border mb-4">
          {messages.map((msg, idx) => (
            <div key={idx} className={`flex mb-3 ${msg.sender === "user" ? "justify-end" : "justify-start"}`}>
              {msg.sender === "bot" && (
                <Image
                  src="/oanhbihi-avatar.png"
                  width={36}
                  height={36}
                  alt="bot"
                  className="rounded-full mr-2"
                />
              )}
              <div className={`px-4 py-2 rounded-lg text-sm max-w-[70%] ${msg.sender === "user" ? "bg-purple-100" : "bg-pink-50 border"}`}>
                {msg.text}
              </div>
            </div>
          ))}

          {loading && (
            <div className="flex items-center gap-2 text-sm text-gray-400">
              <Image src="/oanhbihi-avatar.png" width={24} height={24} alt="typing" />
              <span>Oanh Bihi đang gõ...</span>
            </div>
          )}
        </div>

        <div className="flex gap-2">
          <input
            type="text"
            value={input}
            onChange={(e) => setInput(e.target.value)}
            className="input input-bordered flex-1"
            placeholder="Nhập câu hỏi của bạn..."
            onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          />
          <button className="btn btn-primary" onClick={sendMessage} disabled={loading}>
            Gửi
          </button>
        </div>
      </div>
    </Layout>
  );
}
