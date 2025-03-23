import Link from "next/link";
import { useRouter } from "next/router";

const Sidebar = () => {
  const router = useRouter();
  const navItems = [
    { label: "Tổng quan", path: "/dashboard" },
    { label: "Cấu hình OpenAI", path: "/dashboard/openai" },
    { label: "Cấu hình Messenger", path: "/dashboard/messenger" },
    { label: "Cấu hình Bot & Personas", path: "/dashboard/bot-config" },
    { label: "Cấu hình Crawl dữ liệu", path: "/dashboard/crawl" },
    { label: "Tài liệu huấn luyện", path: "/dashboard/training" },
    { label: "Logs", path: "/dashboard/logs" },
  ];

  return (
    <aside className="w-64 h-screen bg-white shadow-md p-4 sticky top-0">
      <h2 className="text-2xl font-bold text-pink-600 mb-6">Oanh Bihi 💖</h2>
      <nav className="space-y-2">
        {navItems.map((item) => (
          <Link key={item.path} href={item.path}>
            <div
              className={`p-2 rounded-lg cursor-pointer font-medium text-sm transition-all ${
                router.pathname === item.path
                  ? "bg-pink-100 text-pink-600"
                  : "text-gray-700 hover:bg-pink-50"
              }`}
            >
              {item.label}
            </div>
          </Link>
        ))}
      </nav>
    </aside>
  );
};

export default Sidebar;