import React, { createContext, useState, useEffect } from "react";
import { api } from "../services/api";

export const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [user, setUser] = useState(null);

  const login = async (username, password) => {
    const res = await api.post("/api/auth/login", { username, password });
    localStorage.setItem("access_token", res.data.access_token);
    setUser(res.data.user);
  };

  const register = async (email, username, password) => {
    await api.post("/api/auth/register", { email, username, password });
  };

  const logout = () => {
    localStorage.removeItem("access_token");
    setUser(null);
  };

  const loadUser = async () => {
    try {
      const res = await api.get("/api/auth/me");
      setUser(res.data.user);
    } catch {
      setUser(null);
    }
  };

  useEffect(() => {
    loadUser();
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, register, logout }}>
      {children}
    </AuthContext.Provider>
  );
};