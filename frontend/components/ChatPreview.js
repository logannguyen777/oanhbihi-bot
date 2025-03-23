export default function ChatPreview({ platform = "Messenger" }) {
    const sampleMessages = [
      { role: "user", content: "Chào Oanh Bihi 👋" },
      { role: "assistant", content: "Chào bạn! Mình là Oanh Bihi nè 💜" },
      { role: "user", content: "Tư vấn giúp mình ngành Tài chính nha!" },
      { role: "assistant", content: "Dạ có ngay~ Ngành Tài chính tại Đại học Đại Nam siêuuuu xịn 😘" },
    ];
  
    const isMessenger = platform === "Messenger";
    const platformColor = isMessenger ? "bg-blue-100" : "bg-green-100";
    const title = isMessenger ? "🟦 Messenger Preview" : "🟩 Zalo Preview";
  
    return (
      <div className={`rounded-xl p-4 shadow-lg ${platformColor}`}>
        <h3 className="text-lg font-semibold mb-3">{title}</h3>
        <div className="space-y-3 bg-white p-3 rounded-lg h-80 overflow-y-auto">
          {sampleMessages.map((msg, i) => (
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
          <div className="chat chat-start">
            <div className="chat-image avatar">
              <div className="w-8 rounded-full">
                <img src="/logo.png" alt="typing" />
              </div>
            </div>
            <div className="chat-bubble chat-bubble-primary animate-pulse">
              Oanh Bihi đang nghĩ... 🤔
            </div>
          </div>
        </div>
      </div>
    );
  }
  