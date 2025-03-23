import { useEffect, useState } from "react";
import Layout from "@/components/Layout";
import AuthGuard from "@/components/AuthGuard";

const tabNames = ["OpenAI", "Facebook", "Zalo", "Bot"];

export default function SettingsPage() {
  const [config, setConfig] = useState({});
  const [activeTab, setActiveTab] = useState("OpenAI");
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/config`, {
      headers: {
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
    })
      .then((res) => res.json())
      .then((data) => setConfig(data));
  }, []);

  const handleChange = (e) => {
    setConfig({ ...config, [e.target.name]: e.target.value });
  };

  const handleToggle = () => {
    setConfig({ ...config, bot_enabled: !config.bot_enabled });
  };

  const handleSave = async () => {
    setLoading(true);
    await fetch(`${process.env.NEXT_PUBLIC_API_BASE_URL}/config`, {
      method: "POST",
      headers: {
        "Content-Type": "application/json",
        Authorization: `Bearer ${localStorage.getItem("token")}`,
      },
      body: JSON.stringify(config),
    });
    setLoading(false);
  };

  const renderTab = () => {
    switch (activeTab) {
      case "OpenAI":
        return (
          <div className="space-y-3">
            <input
              name="openai_api_key"
              value={config.openai_api_key || ""}
              onChange={handleChange}
              placeholder="OpenAI API Key"
              className="input input-bordered w-full"
            />
          </div>
        );
      case "Facebook":
        return (
          <div className="space-y-3">
            <input
              name="fb_page_token"
              value={config.fb_page_token || ""}
              onChange={handleChange}
              placeholder="FB Page Token"
              className="input input-bordered w-full"
            />
            <input
              name="fb_verify_token"
              value={config.fb_verify_token || ""}
              onChange={handleChange}
              placeholder="FB Verify Token"
              className="input input-bordered w-full"
            />
          </div>
        );
      case "Zalo":
        return (
          <div className="space-y-3">
            <input
              name="zalo_oa_id"
              value={config.zalo_oa_id || ""}
              onChange={handleChange}
              placeholder="Zalo OA ID"
              className="input input-bordered w-full"
            />
            <input
              name="zalo_access_token"
              value={config.zalo_access_token || ""}
              onChange={handleChange}
              placeholder="Zalo Access Token"
              className="input input-bordered w-full"
            />
            <input
              name="zalo_verify_token"
              value={config.zalo_verify_token || ""}
              onChange={handleChange}
              placeholder="Zalo Verify Token"
              className="input input-bordered w-full"
            />
          </div>
        );
      case "Bot":
        return (
          <div className="form-control">
            <label className="label cursor-pointer">
              <span className="label-text">Kích hoạt bot trả lời?</span>
              <input
                type="checkbox"
                className="toggle toggle-primary"
                checked={config.bot_enabled || false}
                onChange={handleToggle}
              />
            </label>
          </div>
        );
    }
  };

  return (
    <AuthGuard>
      <Layout>
        <div className="max-w-2xl mx-auto bg-white p-6 rounded-xl shadow space-y-6">
          <h2 className="text-2xl font-bold text-purple-600">⚙️ Cấu hình hệ thống</h2>

          <div className="tabs tabs-boxed">
            {tabNames.map((tab) => (
              <a
                key={tab}
                className={`tab ${activeTab === tab ? "tab-active" : ""}`}
                onClick={() => setActiveTab(tab)}
              >
                {tab}
              </a>
            ))}
          </div>

          <div>{renderTab()}</div>

          <button
            className={`btn btn-primary w-full ${loading ? "loading" : ""}`}
            onClick={handleSave}
          >
            Lưu cấu hình
          </button>
        </div>
      </Layout>
    </AuthGuard>
  );
}
