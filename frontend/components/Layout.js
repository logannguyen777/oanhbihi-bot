import Sidebar from "./Sidebar";

export default function Layout({ children }) {
  return (
    <div className="flex min-h-screen">
      <Sidebar />
      <main className="flex-1 bg-gray-50 p-6 overflow-y-auto">{children}</main>
    </div>
  );
}
