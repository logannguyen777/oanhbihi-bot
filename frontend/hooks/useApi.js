export async function apiFetch(path, method = "GET", body) {
    const token = localStorage.getItem("token");
    const res = await fetch(`http://localhost:8000${path}`, {
      method,
      headers: {
        "Content-Type": "application/json",
        Authorization: token ? `Bearer ${token}` : "",
      },
      body: body ? JSON.stringify(body) : undefined,
    });
  
    if (!res.ok) {
      throw new Error(await res.text());
    }
  
    return res.json();
  }
  