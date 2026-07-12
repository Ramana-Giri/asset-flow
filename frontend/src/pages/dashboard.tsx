import { useAuth } from "../context/AuthContext";
import { useNavigate } from "react-router-dom";   

import { 
  LayoutDashboard, 
  Building2, 
  Package, 
  ArrowLeftRight, 
  Calendar, 
  Wrench, 
  ClipboardCheck, 
  BarChart3, 
  Bell,
  Plus,
  BookOpen,
  AlertTriangle,
  ChevronRight,
  Users,
  Clock,
} from "lucide-react";
import { useState } from "react";

// Sample data
const stats = {
  available: 128,
  allocated: 76,
  maintenance: 4,
  activeBookings: 9,
  pendingTransfers: 3,
  upcomingReturns: 12
};

const recentActivities = [
  { id: 1, asset: "Laptop AF-0114", action: "allocated to Room B2", status: "booking confirmed", time: "2:00 to 3:00 PM", type: "booking" },
  { id: 2, asset: "Projector AF-0062", action: "maintenance resolved", status: "completed", time: "1 hour ago", type: "maintenance" },
  { id: 3, asset: "MacBook AF-0089", action: "returned by John Doe", status: "pending verification", time: "30 min ago", type: "return" },
  { id: 4, asset: "Desk AF-0023", action: "allocated to Team Alpha", status: "approved", time: "2 hours ago", type: "allocation" },
];

const upcomingReturns = [
  { id: 1, asset: "Laptop AF-0114", user: "Sarah Johnson", due: "Today, 5:00 PM", status: "urgent" },
  { id: 2, asset: "Projector AF-0062", user: "Mike Chen", due: "Tomorrow, 10:00 AM", status: "pending" },
  { id: 3, asset: "iPad AF-0078", user: "Emma Wilson", due: "Tomorrow, 6:00 PM", status: "pending" },
];

const assetDistribution = [
  { category: "Electronics", count: 45, color: "bg-purple-500" },
  { category: "Furniture", count: 32, color: "bg-indigo-500" },
  { category: "Vehicles", count: 18, color: "bg-blue-500" },
  { category: "Equipment", count: 27, color: "bg-violet-500" },
  { category: "Others", count: 22, color: "bg-pink-500" },
];

const navItems = [
  { icon: LayoutDashboard, label: "Dashboard", active: true },
  { icon: Building2, label: "Organization Setup" },
  { icon: Package, label: "Assets" },
  { icon: ArrowLeftRight, label: "Allocation & Transfer" },
  { icon: Calendar, label: "Resource Booking" },
  { icon: Wrench, label: "Maintenance" },
  { icon: ClipboardCheck, label: "Audit" },
  { icon: BarChart3, label: "Reports" },
  { icon: Bell, label: "Notifications" },
];

const getRoute = (label: string) => {
  switch (label) {
    case "Dashboard": return "/dashboard";
    case "Organization Setup": return "/organization";
    case "Assets": return "/assets";
    case "Allocation & Transfer": return "/allocations";
    case "Resource Booking": return "/bookings";
    case "Maintenance": return "/maintenance";
    case "Audit": return "/audits";
    case "Reports": return "/reports";
    case "Notifications": return "/notifications";
    default: return "/dashboard";
  }
};

export default function Dashboard() {
  const { user, logoutUser } = useAuth();
  const [isSidebarOpen, setIsSidebarOpen] = useState(true);
  const navigate = useNavigate();   

  return (
    <div className="min-h-screen bg-[#0a0a0f] text-gray-100 flex">
      {/* Sidebar */}
      <aside className={`${isSidebarOpen ? 'w-72' : 'w-20'} bg-[#1a1a2e] border-r border-purple-900/30 transition-all duration-300 flex flex-col h-screen sticky top-0`}>
        <div className="p-6 border-b border-purple-900/30 flex items-center gap-3">
          <div className="w-10 h-10 rounded-xl bg-gradient-to-br from-purple-500 to-indigo-600 flex items-center justify-center">
            <span className="text-white font-bold text-lg">AF</span>
          </div>
          {isSidebarOpen && (
            <span className="text-xl font-bold bg-gradient-to-r from-purple-400 to-indigo-400 bg-clip-text text-transparent">
              AssetFlow
            </span>
          )}
        </div>

        <nav className="flex-1 p-4 space-y-1 overflow-y-auto">
          {navItems.map((item, index) => (
            <button
              key={index}
              onClick={() => navigate(getRoute(item.label))}
              className={`w-full flex items-center gap-3 px-4 py-3 rounded-xl transition-all duration-200 ${
                item.active 
                  ? 'bg-purple-600/20 text-purple-400 border border-purple-500/30' 
                  : 'text-gray-400 hover:bg-purple-600/10 hover:text-gray-200'
              }`}
            >
              <item.icon className="w-5 h-5 flex-shrink-0" />
              {isSidebarOpen && (
                <span className="text-sm font-medium">{item.label}</span>
              )}
            </button>
          ))}
        </nav>

        <div className="p-4 border-t border-purple-900/30">
          <button 
            onClick={() => setIsSidebarOpen(!isSidebarOpen)}
            className="w-full text-gray-400 hover:text-gray-200 text-sm flex items-center justify-center gap-2"
          >
            <ChevronRight className={`w-4 h-4 transition-transform ${isSidebarOpen ? 'rotate-180' : ''}`} />
            {isSidebarOpen && <span>Collapse</span>}
          </button>
        </div>
      </aside>

      {/* Main Content */}
      <main className="flex-1 overflow-y-auto">
        {/* Top Bar */}
        <header className="bg-[#1a1a2e]/80 backdrop-blur-lg border-b border-purple-900/30 sticky top-0 z-10">
          <div className="px-8 py-4 flex items-center justify-between">
            <div>
              <h1 className="text-2xl font-bold text-gray-100">Dashboard</h1>
              <p className="text-gray-400 text-sm">Welcome back, {user}</p>
            </div>
            <div className="flex items-center gap-4">
              <button className="relative p-2 rounded-xl hover:bg-purple-600/10 transition-colors">
                <Bell className="w-5 h-5 text-gray-400" />
                <span className="absolute top-1 right-1 w-2 h-2 bg-red-500 rounded-full"></span>
              </button>
              <button 
                onClick={logoutUser} 
                className="bg-red-500/10 text-red-400 px-4 py-2 rounded-xl hover:bg-red-500/20 transition-colors text-sm font-medium border border-red-500/20"
              >
                Logout
              </button>
            </div>
          </div>
        </header>

        <div className="p-8 space-y-8">
          {/* KPI Cards */}
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
            <div className="bg-[#1a1a2e] rounded-2xl p-6 border border-purple-900/30">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-400 text-sm">Available Assets</span>
                <Package className="w-5 h-5 text-emerald-400" />
              </div>
              <div className="text-3xl font-bold text-gray-100">{stats.available}</div>
              <div className="flex items-center gap-2 mt-2 text-sm text-emerald-400">
                <span>↑ 12%</span>
                <span className="text-gray-500">from last month</span>
              </div>
            </div>

            <div className="bg-[#1a1a2e] rounded-2xl p-6 border border-purple-900/30">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-400 text-sm">Allocated</span>
                <Users className="w-5 h-5 text-blue-400" />
              </div>
              <div className="text-3xl font-bold text-gray-100">{stats.allocated}</div>
              <div className="flex items-center gap-2 mt-2 text-sm text-blue-400">
                <span>↑ 8%</span>
                <span className="text-gray-500">from last month</span>
              </div>
            </div>

            <div className="bg-[#1a1a2e] rounded-2xl p-6 border border-purple-900/30">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-400 text-sm">In Maintenance</span>
                <Wrench className="w-5 h-5 text-amber-400" />
              </div>
              <div className="text-3xl font-bold text-gray-100">{stats.maintenance}</div>
              <div className="flex items-center gap-2 mt-2 text-sm text-amber-400">
                <span>↓ 3%</span>
                <span className="text-gray-500">from last month</span>
              </div>
            </div>

            <div className="bg-[#1a1a2e] rounded-2xl p-6 border border-purple-900/30">
              <div className="flex items-center justify-between mb-2">
                <span className="text-gray-400 text-sm">Active Bookings</span>
                <Calendar className="w-5 h-5 text-purple-400" />
              </div>
              <div className="text-3xl font-bold text-gray-100">{stats.activeBookings}</div>
              <div className="flex items-center gap-2 mt-2 text-sm text-purple-400">
                <span>↑ 5%</span>
                <span className="text-gray-500">from last month</span>
              </div>
            </div>
          </div>

          {/* Secondary Stats */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
            <div className="bg-[#1a1a2e] rounded-2xl p-6 border border-purple-900/30">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Pending Transfers</p>
                  <p className="text-2xl font-bold text-gray-100 mt-1">{stats.pendingTransfers}</p>
                </div>
                <div className="w-12 h-12 rounded-xl bg-blue-500/10 flex items-center justify-center">
                  <ArrowLeftRight className="w-6 h-6 text-blue-400" />
                </div>
              </div>
            </div>

            <div className="bg-[#1a1a2e] rounded-2xl p-6 border border-purple-900/30">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Upcoming Returns</p>
                  <p className="text-2xl font-bold text-gray-100 mt-1">{stats.upcomingReturns}</p>
                </div>
                <div className="w-12 h-12 rounded-xl bg-amber-500/10 flex items-center justify-center">
                  <Clock className="w-6 h-6 text-amber-400" />
                </div>
              </div>
            </div>

            <div className="bg-[#1a1a2e] rounded-2xl p-6 border border-purple-900/30">
              <div className="flex items-center justify-between">
                <div>
                  <p className="text-gray-400 text-sm">Overdue Returns</p>
                  <p className="text-2xl font-bold text-red-400 mt-1">3</p>
                </div>
                <div className="w-12 h-12 rounded-xl bg-red-500/10 flex items-center justify-center">
                  <AlertTriangle className="w-6 h-6 text-red-400" />
                </div>
              </div>
              <p className="text-xs text-red-400/70 mt-2">⚠️ 3 assets overdue for return - flagged for follow-up</p>
            </div>
          </div>

          {/* Charts and Activity */}
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-6">
            {/* Asset Distribution Chart */}
            <div className="lg:col-span-1 bg-[#1a1a2e] rounded-2xl p-6 border border-purple-900/30">
              <h3 className="text-gray-200 font-semibold mb-4">Asset Distribution</h3>
              <div className="space-y-4">
                {assetDistribution.map((item, index) => (
                  <div key={index} className="space-y-1">
                    <div className="flex justify-between text-sm">
                      <span className="text-gray-400">{item.category}</span>
                      <span className="text-gray-200 font-medium">{item.count}</span>
                    </div>
                    <div className="w-full h-2 bg-gray-700 rounded-full overflow-hidden">
                      <div 
                        className={`h-full ${item.color} rounded-full transition-all duration-500`}
                        style={{ width: `${(item.count / 144) * 100}%` }}
                      ></div>
                    </div>
                  </div>
                ))}
              </div>
            </div>

            {/* Recent Activity */}
            <div className="lg:col-span-2 bg-[#1a1a2e] rounded-2xl p-6 border border-purple-900/30">
              <div className="flex items-center justify-between mb-4">
                <h3 className="text-gray-200 font-semibold">Recent Activity</h3>
                <button className="text-purple-400 text-sm hover:text-purple-300 transition-colors">View All</button>
              </div>
              <div className="space-y-4">
                {recentActivities.map((activity) => (
                  <div key={activity.id} className="flex items-start gap-3 p-3 rounded-xl hover:bg-purple-600/5 transition-colors">
                    <div className={`w-2 h-2 rounded-full mt-2 flex-shrink-0 ${
                      activity.type === 'booking' ? 'bg-blue-400' :
                      activity.type === 'maintenance' ? 'bg-emerald-400' :
                      activity.type === 'return' ? 'bg-amber-400' : 'bg-purple-400'
                    }`}></div>
                    <div className="flex-1">
                      <p className="text-sm text-gray-200">
                        <span className="font-medium text-purple-400">{activity.asset}</span>
                        <span className="text-gray-400"> - {activity.action}</span>
                      </p>
                      <div className="flex items-center gap-2 mt-1">
                        <span className={`text-xs px-2 py-0.5 rounded-full ${
                          activity.status === 'booking confirmed' ? 'bg-blue-500/20 text-blue-400' :
                          activity.status === 'completed' ? 'bg-emerald-500/20 text-emerald-400' :
                          activity.status === 'pending verification' ? 'bg-amber-500/20 text-amber-400' :
                          'bg-purple-500/20 text-purple-400'
                        }`}>
                          {activity.status}
                        </span>
                        <span className="text-xs text-gray-500">{activity.time}</span>
                      </div>
                    </div>
                  </div>
                ))}
              </div>
            </div>
          </div>

          {/* Upcoming Returns */}
          <div className="bg-[#1a1a2e] rounded-2xl p-6 border border-purple-900/30">
            <div className="flex items-center justify-between mb-4">
              <h3 className="text-gray-200 font-semibold">Upcoming Returns</h3>
              <button className="text-purple-400 text-sm hover:text-purple-300 transition-colors">View All</button>
            </div>
            <div className="overflow-x-auto">
              <table className="w-full">
                <thead>
                  <tr className="text-left text-xs text-gray-500 border-b border-purple-900/30">
                    <th className="pb-3 font-medium">Asset</th>
                    <th className="pb-3 font-medium">User</th>
                    <th className="pb-3 font-medium">Due Date</th>
                    <th className="pb-3 font-medium">Status</th>
                  </tr>
                </thead>
                <tbody className="divide-y divide-purple-900/20">
                  {upcomingReturns.map((item) => (
                    <tr key={item.id} className="hover:bg-purple-600/5 transition-colors">
                      <td className="py-3 text-sm text-gray-200">{item.asset}</td>
                      <td className="py-3 text-sm text-gray-400">{item.user}</td>
                      <td className="py-3 text-sm text-gray-400">{item.due}</td>
                      <td className="py-3">
                        <span className={`text-xs px-2 py-1 rounded-full ${
                          item.status === 'urgent' ? 'bg-red-500/20 text-red-400' : 'bg-amber-500/20 text-amber-400'
                        }`}>
                          {item.status}
                        </span>
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          {/* Quick Actions */}
          <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
            <button className="bg-gradient-to-r from-purple-600 to-indigo-600 p-4 rounded-2xl flex items-center justify-center gap-3 hover:shadow-lg hover:shadow-purple-500/20 transition-all">
              <Plus className="w-5 h-5" />
              <span className="font-medium">Register Asset</span>
            </button>
            <button
              onClick={() => navigate("/bookings")}
              className="bg-[#1a1a2e] border border-purple-900/30 p-4 rounded-2xl flex items-center justify-center gap-3 hover:bg-purple-600/10 transition-all"
            >
              <BookOpen className="w-5 h-5" />
              <span className="font-medium">Book Resource</span>
            </button>
            <button className="bg-[#1a1a2e] border border-purple-900/30 p-4 rounded-2xl flex items-center justify-center gap-3 hover:bg-purple-600/10 transition-all">
              <AlertTriangle className="w-5 h-5" />
              <span className="font-medium">Raise Request</span>
            </button>
          </div>
        </div>
      </main>
    </div>
  );
}
