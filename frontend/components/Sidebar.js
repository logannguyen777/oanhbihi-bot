import Link from "next/link";
import { useRouter } from "next/router";

const items = [
  { label: "Dashboard", href: "/dashboard" },
  { label: "Chatbot", href: "/chat" },
  { label: "Cấu hình", href: "/settings" },
  { label: "Admin Chat", href: "/admin_chat" },
];

export default function Sidebar() {
  const router = useRouter();
  return (
    <div className="w-64 bg-white border-r shadow-md p-4 space-y-4">
      <h2 className="text-2xl font-bold text-purple-600">🌸 Oanh Bihi</h2>
      <ul className="menu">
        {items.map((item) => (
          <li key={item.href}>
            <Link
              href={item.href}
              className={`${
                router.pathname === item.href ? "active bg-purple-200" : ""
              }`}
            >
              {item.label}
            </Link>
          </li>
        ))}
      </ul>
    </div>
  );
}
