import { createContext, useContext, useState, type ReactNode } from "react";
import { logout as serviceLogout, getToken } from "../services/auth";

interface AuthContextType {
  user: string | null;
  loginUser: (email: string) => void;
  logoutUser: () => void;
}

const AuthContext = createContext<AuthContextType | undefined>(undefined);

export function AuthProvider({ children }: { children: ReactNode }) {
  const [user, setUser] = useState<string | null>(() => {
    return getToken() ? "user@example.com" : null; // dummy until real user fetch
  });

  const loginUser = (email: string) => {
    setUser(email);
  };

  const logoutUser = () => {
    serviceLogout();
    setUser(null);
  };

  return (
    <AuthContext.Provider value={{ user, loginUser, logoutUser }}>
      {children}
    </AuthContext.Provider>
  );
}

export const useAuth = () => {
  const context = useContext(AuthContext);
  if (!context) throw new Error("useAuth must be used within AuthProvider");
  return context;
};
