import { useState, useEffect } from 'react';

export default function ZaloConfig() {
  const [config, setConfig] = useState({
    zalo_oa_id: '',
    zalo_access_token: '',
    zalo_verify_token: '',
  });

  useEffect(() => {
    fetch('/api/config')
      .then(res => res.json())
      .then(data => {
        setConfig({
          zalo_oa_id: data.zalo_oa_id || '',
          zalo_access_token: data.zalo_access_token || '',
          zalo_verify_token: data.zalo_verify_token || '',
        });
      });
  }, []);

  const handleSave = async () => {
    await fetch('/api/config', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(config),
    });
    alert('Đã lưu cấu hình Zalo!');
  };

  return (
    <div className="p-6">
      <h2 className="text-xl font-semibold mb-4">⚙️ Cấu hình Zalo OA</h2>
      <div className="space-y-4 max-w-md">
        <div>
          <label className="block mb-1 text-sm">Zalo OA ID</label>
          <input
            className="w-full border rounded px-3 py-2"
            value={config.zalo_oa_id}
            onChange={(e) => setConfig({ ...config, zalo_oa_id: e.target.value })}
          />
        </div>
        <div>
          <label className="block mb-1 text-sm">Access Token</label>
          <input
            className="w-full border rounded px-3 py-2"
            value={config.zalo_access_token}
            onChange={(e) => setConfig({ ...config, zalo_access_token: e.target.value })}
          />
        </div>
        <div>
          <label className="block mb-1 text-sm">Verify Token</label>
          <input
            className="w-full border rounded px-3 py-2"
            value={config.zalo_verify_token}
            onChange={(e) => setConfig({ ...config, zalo_verify_token: e.target.value })}
          />
        </div>
        <button
          className="mt-4 px-4 py-2 bg-blue-600 text-white rounded hover:bg-blue-700"
          onClick={handleSave}
        >
          Lưu cấu hình
        </button>
      </div>
    </div>
  );
}
