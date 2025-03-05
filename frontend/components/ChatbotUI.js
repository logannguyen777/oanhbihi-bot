import { useState, useEffect, useRef } from "react";
import { motion } from "framer-motion";
import { Send, User, Bot } from "lucide-react";

export default function ChatbotUI() {
  const [messages, setMessages] = useState([]);
  const [input, setInput] = useState("");
  const [isTyping, setIsTyping] = useState(false);
  const chatEndRef = useRef(null);

  useEffect(() => {
    chatEndRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim()) return;

    const newMessage = { role: "user", content: input };
    setMessages((prev) => [...prev, newMessage]);
    setInput("");
    setIsTyping(true);

    try {
      const response = await fetch("http://localhost:8000/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ input_text: input }),
      });
      const data = await response.json();
      setIsTyping(false);
      if (data.response) {
        setMessages((prev) => [...prev, { role: "bot", content: data.response }]);
      }
    } catch (error) {
      setIsTyping(false);
      console.error("Lỗi gửi tin nhắn:", error);
    }
  };

  const handleKeyPress = (event) => {
    if (event.key === "Enter") {
      event.preventDefault();
      sendMessage();
    }
  };

  return (
    <div className="flex flex-col max-w-lg mx-auto h-[80vh] bg-white shadow-xl rounded-lg border border-gray-200 fixed top-1/2 left-1/2 transform -translate-x-1/2 -translate-y-1/2 w-full max-w-md">
      <div className="p-4 bg-blue-600 text-white text-center text-lg font-semibold rounded-t-lg">Chat với Oanh Bihi 🤖</div>
      <div className="flex-1 p-4 space-y-4 overflow-y-auto bg-gray-50" style={{ maxHeight: "65vh" }}>
        {messages.map((msg, index) => (
          <motion.div
            key={index}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ duration: 0.3 }}
            className={`flex ${msg.role === "user" ? "justify-end" : "justify-start"}`}
          >
            <div className="flex items-center max-w-xs space-x-2">
              {msg.role === "bot" && <Bot className="w-10 h-10 text-gray-500 bg-gray-300 rounded-full p-2" />}
              <div className={`p-3 rounded-xl ${msg.role === "user" ? "bg-blue-600 text-white" : "bg-gray-200 text-black"}`}>{msg.content}</div>
              {msg.role === "user" && <User className="w-10 h-10 text-white bg-blue-600 rounded-full p-2" />}
            </div>
          </motion.div>
        ))}
        {isTyping && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ duration: 0.5, repeat: Infinity, repeatType: "reverse" }}
            className="flex items-center space-x-2"
          >
            <Bot className="w-10 h-10 text-gray-500 bg-gray-300 rounded-full p-2" />
            <span className="text-gray-500 italic">Oanh Bihi đang phản hồi...</span>
          </motion.div>
        )}
        <div ref={chatEndRef} />
      </div>
      <div className="p-3 flex items-center gap-2 bg-white border-t rounded-b-lg sticky bottom-0 w-full">
        <input
          className="flex-1 p-3 border rounded-full focus:outline-none focus:ring-2 focus:ring-blue-500"
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyPress={handleKeyPress}
          placeholder="Nhập tin nhắn..."
        />
        <button onClick={sendMessage} className="p-3 rounded-full bg-blue-600 text-white shadow-lg hover:bg-blue-700">
          <Send size={20} />
        </button>
      </div>
    </div>
  );
}
