import { Navigate } from "react-router-dom";
import { getToken } from "../services/auth";
import type { JSX } from "react/jsx-runtime";

export default function ProtectedRoute({
  children,
}: {
  children: JSX.Element;
}) {
  if (!getToken()) {
    return <Navigate to="/login" replace />;
  }
  return children;
}
