// pages/dashboard/index.js
import Head from "next/head";
import DashboardLayout from "../../components/layout/DashboardLayout";

export default function DashboardHome() {
  return (
    <DashboardLayout>
      <Head><title>Oanh Bihi Dashboard</title></Head>
      <div className="bg-white shadow rounded-xl p-6">
        <h1 className="text-2xl font-bold text-pink-600 mb-2">🎀 Chào mừng đến với Oanh Bihi Dashboard</h1>
        <p className="text-gray-700">Cùng khám phá và cấu hình cô trợ lý dễ thương này nhé!</p>
      </div>
    </DashboardLayout>
  );
}
