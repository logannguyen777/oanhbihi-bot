import Layout from "@/components/Layout";
import AuthGuard from "@/components/AuthGuard";

export default function Dashboard() {
  return (
    <AuthGuard>
      <Layout>
        <h2 className="text-2xl font-bold mb-4">🎯 Dashboard chính</h2>
        <p>Chào mừng đến với hệ thống quản trị Oanh Bihi Bot nèee~</p>
      </Layout>
    </AuthGuard>
  );
}
