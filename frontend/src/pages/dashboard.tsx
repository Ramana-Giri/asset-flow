import { useAuth } from "../context/AuthContext";

export default function Dashboard() {
  const { user, logoutUser } = useAuth();

  return (
    <div className="min-h-screen bg-gray-50">
      <nav className="bg-white shadow-sm border-b border-gray-200 sticky top-0 z-10">
        <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 flex justify-between h-16 items-center">
          <h1 className="text-xl font-bold text-indigo-600">AssetFlow</h1>
          <div className="flex items-center gap-4">
            <span className="text-sm text-gray-600 hidden sm:block">{user}</span>
            <button onClick={logoutUser} className="bg-red-100 text-red-700 px-4 py-2 rounded-lg hover:bg-red-200 text-sm font-medium">
              Logout
            </button>
          </div>
        </div>
      </nav>
      <main className="max-w-7xl mx-auto py-8 px-4">
        <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-8">
          <h2 className="text-2xl font-bold text-gray-800">Welcome to AssetFlow</h2>
          <p className="text-gray-500 mt-1">Your dashboard is ready. Build your features here.</p>
        </div>
      </main>
    </div>
  );
}