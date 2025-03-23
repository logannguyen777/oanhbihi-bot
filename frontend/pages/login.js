// frontend/pages/login.js
import { useState } from "react";
import { useRouter } from "next/router";
import Head from "next/head";

const HARDCODED = {
  username: "admin",
  password: "oanhbihi",
};

export default function LoginPage() {
  const [form, setForm] = useState({ username: "", password: "" });
  const [error, setError] = useState("");
  const router = useRouter();

  const handleLogin = () => {
    if (
      form.username === HARDCODED.username &&
      form.password === HARDCODED.password
    ) {
      localStorage.setItem("oanhbihi_token", "dummy-token");
      router.push("/dashboard");
    } else {
      setError("Sai tài khoản hoặc mật khẩu rồi anh yêu ơi 😢");
    }
  };

  return (
    <>
      <Head>
        <title>Đăng nhập | Oanh Bihi</title>
      </Head>
      <div className="min-h-screen flex items-center justify-center bg-pink-50">
        <div className="bg-white shadow-lg rounded-xl px-10 py-8 w-full max-w-sm">
          <h1 className="text-2xl font-bold text-center text-pink-600 mb-6">
            🧚‍♀️ Oanh Bihi Đăng Nhập
          </h1>
          <input
            type="text"
            placeholder="Tên đăng nhập"
            className="w-full p-2 border rounded mb-4"
            value={form.username}
            onChange={(e) => setForm({ ...form, username: e.target.value })}
          />
          <input
            type="password"
            placeholder="Mật khẩu"
            className="w-full p-2 border rounded mb-4"
            value={form.password}
            onChange={(e) => setForm({ ...form, password: e.target.value })}
          />
          <button
            onClick={handleLogin}
            className="bg-pink-500 hover:bg-pink-600 text-white font-medium w-full py-2 rounded"
          >
            Đăng nhập
          </button>
          {error && <p className="text-red-500 text-sm mt-3 text-center">{error}</p>}
        </div>
      </div>
    </>
  );
}
