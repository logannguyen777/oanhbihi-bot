import { useEffect } from "react";
import { useRouter } from "next/router";

export default function AuthGuard({ children }) {
  const router = useRouter();

  useEffect(() => {
    const token = localStorage.getItem("token");
    if (!token) router.push("/login");
  }, []);

  return <>{children}</>;
}
