import { useEffect, useState, useRef } from "react";
import Layout from "@/components/Layout";
import AuthGuard from "@/components/AuthGuard";

export default function ChatPage() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef();

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const handleSend = async () => {
    if (!input.trim()) return;

    const userMsg = { role: "user", content: input };
    setMessages((prev) => [...prev, userMsg]);
    setInput("");
    setIsTyping(true);

    try {
      const res = await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
          Authorization: `Bearer ${localStorage.getItem("token")}`,
        },
        body: JSON.stringify({ message: input }),
      });
      const data = await res.json();
      setMessages((prev) => [...prev, { role: "assistant", content: data.answer }]);
    } catch (err) {
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: "Oops! Có lỗi xảy ra 😢" },
      ]);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyDown = (e) => {
    if (e.key === "Enter" && !e.shiftKey) {
      e.preventDefault();
      handleSend();
    }
  };

  return (
    <AuthGuard>
      <Layout>
        <div className="h-[80vh] flex flex-col bg-white rounded-xl shadow-lg p-4">
          <div className="flex-1 overflow-y-auto space-y-4 px-2">
            {messages.map((msg, i) => (
              <div key={i} className={`chat ${msg.role === "user" ? "chat-end" : "chat-start"}`}>
                <div className="chat-image avatar">
                  <div className="w-10 rounded-full">
                    <img
                      alt="avatar"
                      src={msg.role === "user" ? "/user.png" : "/logo.png"}
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
            {isTyping && (
              <div className="chat chat-start">
                <div className="chat-image avatar">
                  <div className="w-10 rounded-full">
                    <img alt="Oanh Bihi" src="/logo.png" />
                  </div>
                </div>
                <div className="chat-bubble chat-bubble-primary animate-pulse">
                  Oanh Bihi đang nghĩ... 🤔
                </div>
              </div>
            )}
            <div ref={chatEndRef} />
          </div>

          <div className="mt-4 flex gap-2">
            <textarea
              value={input}
              onChange={(e) => setInput(e.target.value)}
              onKeyDown={handleKeyDown}
              placeholder="Nhập câu hỏi cho Oanh Bihi..."
              className="textarea textarea-bordered w-full resize-none"
              rows={2}
            />
            <button className="btn btn-primary" onClick={handleSend}>
              Gửi 💌
            </button>
          </div>
        </div>
      </Layout>
    </AuthGuard>
  );
}
