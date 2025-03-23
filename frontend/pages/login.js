import { useRouter } from "next/router";
import { useState } from "react";

export default function LoginPage() {
  const router = useRouter();
  const [formData, setFormData] = useState({ username: "", password: "" });
  const [error, setError] = useState("");

  const handleChange = (e) =>
    setFormData({ ...formData, [e.target.name]: e.target.value });

  const handleLogin = async (e) => {
    e.preventDefault();
    try {
      const res = await fetch("http://localhost:8000/auth/login", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });

      const data = await res.json();
      if (!res.ok) throw new Error(data.detail || "Login failed");

      localStorage.setItem("token", data.access_token); // nếu có
      router.push("/dashboard");
    } catch (err) {
      setError(err.message);
    }
  };

  return (
    <div className="h-screen flex items-center justify-center bg-gradient-to-br from-purple-100 to-white">
      <div className="card w-full max-w-md bg-white shadow-xl p-8 space-y-4">
        <h2 className="text-2xl font-bold text-center text-purple-600">
          Đăng nhập hệ thống Oanh Bihi 💜
        </h2>
        <form className="space-y-4" onSubmit={handleLogin}>
          <input
            type="text"
            name="username"
            placeholder="Tên đăng nhập"
            className="input input-bordered w-full"
            onChange={handleChange}
          />
          <input
            type="password"
            name="password"
            placeholder="Mật khẩu"
            className="input input-bordered w-full"
            onChange={handleChange}
          />
          {error && <p className="text-red-500 text-sm">{error}</p>}
          <button className="btn btn-primary w-full">Đăng nhập</button>
        </form>
      </div>
    </div>
  );
}
