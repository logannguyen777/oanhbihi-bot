import Link from "next/link";
import { useRouter } from "next/router";

const navItems = [
  { name: "Tổng quan", href: "/dashboard" },
  { name: "Cấu hình OpenAI", href: "/dashboard/openai" },
  { name: "Cấu hình Messenger", href: "/dashboard/messenger" },
  { name: "Cấu hình Bot & Personas", href: "/dashboard/bot-config" },
  { name: "Cấu hình Crawl dữ liệu", href: "/dashboard/crawl" },
  { name: "Tài liệu huấn luyện", href: "/dashboard/training" },
  { name: "Logs", href: "/dashboard/logs" },
];

export default function DashboardLayout({ children }) {
  const router = useRouter();

  return (
    <div className="min-h-screen flex bg-gray-100">
      <aside className="w-64 bg-white shadow-xl px-4 py-6">
        <h2 className="text-2xl font-bold text-pink-600 mb-6">Oanh Bihi 💖</h2>
        <nav className="space-y-2">
          {navItems.map((item) => (
            <Link key={item.href} href={item.href}>
              <div
                className={`block px-3 py-2 rounded-lg text-sm font-medium cursor-pointer hover:bg-pink-100 hover:text-pink-600 transition ${
                  router.pathname === item.href
                    ? "bg-pink-50 text-pink-700"
                    : "text-gray-700"
                }`}
              >
                {item.name}
              </div>
            </Link>
          ))}
        </nav>
      </aside>
      <main className="flex-1 px-8 py-6">{children}</main>
    </div>
  );
}
