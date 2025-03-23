// frontend/pages/dashboard/crawl.js
import { useState } from "react";
import Head from "next/head";
import DashboardLayout from "../../components/layout/DashboardLayout";

export default function CrawlConfig() {
  const [urls, setUrls] = useState([""]);
  const [fileTypes, setFileTypes] = useState(["pdf", "html"]);
  const [schedule, setSchedule] = useState("hàng tuần");
  const [status, setStatus] = useState("");

  const handleAddUrl = () => setUrls([...urls, ""]);
  const handleUrlChange = (index, value) => {
    const newUrls = [...urls];
    newUrls[index] = value;
    setUrls(newUrls);
  };

  const handleSubmit = async () => {
    try {
      const res = await fetch("/api/config/crawl", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ urls, fileTypes, schedule }),
      });
      const data = await res.json();
      setStatus(data.message || "Crawl dữ liệu thành công!");
    } catch (err) {
      setStatus("Có lỗi xảy ra khi crawl.");
    }
  };

  return (
    <DashboardLayout>
      <Head><title>Cấu hình Crawl</title></Head>
      <div className="bg-white shadow rounded-xl p-6 max-w-2xl space-y-6">
        <h1 className="text-xl font-bold text-pink-600">🕸️ Cấu hình Crawl dữ liệu</h1>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Danh sách URL</label>
          {urls.map((url, index) => (
            <input
              key={index}
              type="text"
              value={url}
              onChange={(e) => handleUrlChange(index, e.target.value)}
              className="w-full mb-2 p-2 border border-gray-300 rounded"
              placeholder="https://..."
            />
          ))}
          <button onClick={handleAddUrl} className="text-pink-500 text-sm">+ Thêm URL</button>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Định dạng cần crawl</label>
          <div className="flex gap-4">
            {["pdf", "html", "docx"].map((type) => (
              <label key={type} className="inline-flex items-center">
                <input
                  type="checkbox"
                  className="mr-2"
                  checked={fileTypes.includes(type)}
                  onChange={() => {
                    setFileTypes((prev) =>
                      prev.includes(type) ? prev.filter(f => f !== type) : [...prev, type]
                    );
                  }}
                />
                {type.toUpperCase()}
              </label>
            ))}
          </div>
        </div>

        <div>
          <label className="block text-sm font-medium text-gray-700 mb-1">Lịch crawl tự động</label>
          <select
            value={schedule}
            onChange={(e) => setSchedule(e.target.value)}
            className="w-full p-2 border border-gray-300 rounded"
          >
            <option>hàng ngày</option>
            <option>hàng tuần</option>
            <option>hàng tháng</option>
          </select>
        </div>

        <button
          onClick={handleSubmit}
          className="bg-pink-500 hover:bg-pink-600 text-white px-4 py-2 rounded"
        >
          Bắt đầu Crawl
        </button>

        {status && <p className="text-green-600 text-sm mt-2">{status}</p>}
      </div>
    </DashboardLayout>
  );
}
