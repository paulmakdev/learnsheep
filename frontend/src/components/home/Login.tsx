import { useState } from "react";
import { useDispatch } from "react-redux";
import { setUser } from "../../features/user/userSlice";

export default function Login() {
  const [email, setEmail] = useState("");
  const [password, setPassword] = useState("");

  const dispatch = useDispatch();

  const handleLogin = async (e: React.FormEvent) => {
    e.preventDefault();

    // basic validation
    if (!email || !password) return alert("Fill all fields");

    try {
      const res = await fetch(`/api/auth/login-web`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      console.log("posted")

      if (!res.ok) throw new Error("Login failed");

      const data = await res.json();

      console.log(data)

      console.log("success")


      const apiUserInfoResponse = await fetch(`/api/me/info`);

      const apiUserInfo = await apiUserInfoResponse.json();

      const user = {
        email: apiUserInfo.email,
        role: apiUserInfo.role,
        displayName: apiUserInfo.display_name,
        createdAt: apiUserInfo.created_at,
      };

      dispatch(setUser(user));

      // redirect
      //window.location.href = "/dashboard";
    } catch (err) {
      alert("Invalid credentials");
    }
  };

  const handleRegister = async (e: React.FormEvent) => {
    e.preventDefault();

    // basic validation
    if (!email || !password) return alert("Fill all fields");

    try {
      const res = await fetch(`/api/auth/register-web`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ email, password }),
      });

      if (!res.ok) throw new Error("Registration failed");

      const data = await res.json();
      console.log(data)

      // store token (example)
      localStorage.setItem("learnsheep-login-token", data.access_token);

      // redirect
      window.location.href = "/dashboard";
    } catch (err) {
      alert("Invalid credentials");
    }
  };

  return (
    <div className="login-container" style={{display: "flex", flexDirection: "column", gap: "var(--standard-padding)"}}>

        <form onSubmit={handleLogin} className="login-card">
          <div style={{display: "flex", flexDirection: "column", gap: "var(--standard-padding)", borderRadius: "var(--mini-padding)"}}>
          <p className="emboldened" style={{margin: "0", backgroundColor: "var(--primary-bg)", padding: "var(--standard-padding)", borderRadius: "var(--mini-padding)", boxShadow: "var(--shadow-card)"}}>Login</p>
          <div style={{padding: "var(--standard-padding)", display: "flex", flexDirection: "column", paddingTop: "0", gap: "var(--mini-padding)"}}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              style={{padding: "var(--mini-padding)"}}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              style={{padding: "var(--mini-padding)"}}
              onChange={(e) => setPassword(e.target.value)}
            />
            <div style={{padding: "var(--mini-padding)"}}>

            </div>

            <button type="submit" className="button selected hover-fade" style={{padding: "var(--mini-padding)"}}>Login</button>
          </div>
          </div>
        </form>

        <form onSubmit={handleRegister} className="register-card">
          <div style={{display: "flex", flexDirection: "column", gap: "var(--standard-padding)", borderRadius: "var(--mini-padding)"}}>
          <p className="emboldened" style={{margin: "0", backgroundColor: "var(--primary-bg)", padding: "var(--standard-padding)", borderRadius: "var(--mini-padding)", boxShadow: "var(--shadow-card)"}}>Register</p>
          <div style={{padding: "var(--standard-padding)", display: "flex", flexDirection: "column", paddingTop: "0", gap: "var(--mini-padding)"}}>
            <input
              type="email"
              placeholder="Email"
              value={email}
              style={{padding: "var(--mini-padding)"}}
              onChange={(e) => setEmail(e.target.value)}
            />

            <input
              type="password"
              placeholder="Password"
              value={password}
              style={{padding: "var(--mini-padding)"}}
              onChange={(e) => setPassword(e.target.value)}
            />
            <div style={{padding: "var(--mini-padding)"}}>

            </div>

            <button type="submit" className="button selected hover-fade" style={{padding: "var(--mini-padding)"}}>Register</button>
          </div>
          </div>
        </form>

    </div>
  );
}
