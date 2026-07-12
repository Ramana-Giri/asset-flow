import { useState, useEffect, type FormEvent } from "react";
import { apiFetch } from "../services/auth";
import type { Asset, Booking, BookingStatus } from "../types";

export default function BookingsPage() {
  const [assets, setAssets] = useState<Asset[]>([]);
  const [selectedAssetId, setSelectedAssetId] = useState<number | "">("");
  const [bookings, setBookings] = useState<Booking[]>([]);
  const [form, setForm] = useState({ start: "", end: "", purpose: "" });
  const [error, setError] = useState("");
  const [success, setSuccess] = useState("");
  const [loading, setLoading] = useState(false);

  // Fetch bookable assets
  useEffect(() => {
    apiFetch("/assets?is_bookable=true")
      .then((res) => res.json())
      .then((data: Asset[]) => setAssets(data))
      .catch(console.error);
  }, []);

  // Fetch bookings for selected asset
  useEffect(() => {
    if (!selectedAssetId) {
      setBookings([]);
      return;
    }
    apiFetch(`/bookings?asset_id=${selectedAssetId}`)
      .then((res) => res.json())
      .then((data: Booking[]) => setBookings(data))
      .catch(console.error);
  }, [selectedAssetId]);

  const handleCreate = async (e: FormEvent) => {
    e.preventDefault();
    setError("");
    setSuccess("");
    if (!selectedAssetId || !form.start || !form.end) {
      return setError("Please fill all required fields");
    }
    setLoading(true);
    try {
      const res = await apiFetch("/bookings", {
        method: "POST",
        body: JSON.stringify({
          asset_id: selectedAssetId,
          start_time: new Date(form.start).toISOString(),
          end_time: new Date(form.end).toISOString(),
          purpose: form.purpose || null,
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Booking failed");
      }
      setSuccess("Booking created!");
      setForm({ start: "", end: "", purpose: "" });
      // Refresh bookings
      const updated = await apiFetch(
        `/bookings?asset_id=${selectedAssetId}`,
      ).then((r) => r.json());
      setBookings(updated);
    } catch (err: any) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const handleCancel = async (bookingId: number) => {
    try {
      const res = await apiFetch(`/bookings/${bookingId}/cancel`, {
        method: "PUT",
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Cancel failed");
      }
      const updated = await apiFetch(
        `/bookings?asset_id=${selectedAssetId}`,
      ).then((r) => r.json());
      setBookings(updated);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const handleReschedule = async (
    bookingId: number,
    start: string,
    end: string,
  ) => {
    try {
      const res = await apiFetch(`/bookings/${bookingId}/reschedule`, {
        method: "PUT",
        body: JSON.stringify({
          start_time: new Date(start).toISOString(),
          end_time: new Date(end).toISOString(),
        }),
      });
      if (!res.ok) {
        const err = await res.json();
        throw new Error(err.detail || "Reschedule failed");
      }
      const updated = await apiFetch(
        `/bookings?asset_id=${selectedAssetId}`,
      ).then((r) => r.json());
      setBookings(updated);
    } catch (err: any) {
      setError(err.message);
    }
  };

  const statusColor = (status: BookingStatus): string => {
    switch (status) {
      case "Upcoming":
        return "bg-blue-100 text-blue-800";
      case "Ongoing":
        return "bg-green-100 text-green-800";
      case "Completed":
        return "bg-gray-100 text-gray-800";
      case "Cancelled":
        return "bg-red-100 text-red-800";
    }
  };

  return (
    <div className="max-w-6xl mx-auto p-4 sm:p-6">
      <h1 className="text-3xl font-bold text-gray-800 mb-8">
        Resource Bookings
      </h1>

      {/* Asset selector */}
      <div className="mb-6">
        <label className="block text-sm font-medium text-gray-700 mb-2">
          Select a bookable resource
        </label>
        <select
          className="w-full md:w-1/2 px-4 py-2 border border-gray-300 rounded-xl bg-white focus:outline-none focus:ring-2 focus:ring-indigo-400"
          value={selectedAssetId}
          onChange={(e) =>
            setSelectedAssetId(e.target.value ? Number(e.target.value) : "")
          }
        >
          <option value="">-- Choose a resource --</option>
          {assets.map((asset) => (
            <option key={asset.id} value={asset.id}>
              {asset.name} ({asset.asset_tag})
            </option>
          ))}
        </select>
      </div>

      {selectedAssetId && (
        <>
          {/* Booking form */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6 mb-8">
            <h2 className="text-xl font-semibold mb-4">New Booking</h2>
            {error && (
              <div className="bg-red-50 border border-red-200 text-red-700 px-4 py-2 rounded-xl mb-4 text-sm">
                {error}
              </div>
            )}
            {success && (
              <div className="bg-green-50 border border-green-200 text-green-700 px-4 py-2 rounded-xl mb-4 text-sm">
                {success}
              </div>
            )}
            <form
              onSubmit={handleCreate}
              className="grid grid-cols-1 md:grid-cols-3 gap-4"
            >
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Start Time
                </label>
                <input
                  type="datetime-local"
                  value={form.start}
                  onChange={(e) => setForm({ ...form, start: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  End Time
                </label>
                <input
                  type="datetime-local"
                  value={form.end}
                  onChange={(e) => setForm({ ...form, end: e.target.value })}
                  className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400"
                  required
                />
              </div>
              <div>
                <label className="block text-sm font-medium text-gray-700 mb-1">
                  Purpose (optional)
                </label>
                <input
                  type="text"
                  value={form.purpose}
                  onChange={(e) =>
                    setForm({ ...form, purpose: e.target.value })
                  }
                  className="w-full px-4 py-2 border border-gray-300 rounded-xl focus:outline-none focus:ring-2 focus:ring-indigo-400"
                  placeholder="e.g., Team meeting"
                />
              </div>
              <div className="md:col-span-3">
                <button
                  type="submit"
                  disabled={loading}
                  className="bg-gradient-to-r from-indigo-600 to-purple-600 text-white px-6 py-2 rounded-xl font-medium hover:from-indigo-700 hover:to-purple-700 disabled:opacity-50 shadow transition-all duration-200"
                >
                  {loading ? "Booking..." : "Book Resource"}
                </button>
              </div>
            </form>
          </div>

          {/* Bookings list */}
          <div className="bg-white rounded-2xl shadow-sm border border-gray-100 p-6">
            <h2 className="text-xl font-semibold mb-4">Existing Bookings</h2>
            {bookings.length === 0 ? (
              <p className="text-gray-500">
                No bookings yet for this resource.
              </p>
            ) : (
              <div className="space-y-3">
                {bookings.map((booking) => (
                  <div
                    key={booking.id}
                    className="flex flex-col sm:flex-row sm:items-center justify-between p-4 bg-gray-50 rounded-xl"
                  >
                    <div>
                      <div className="flex items-center gap-2 flex-wrap">
                        <span
                          className={`text-xs font-medium px-2 py-0.5 rounded-full ${statusColor(booking.status)}`}
                        >
                          {booking.status}
                        </span>
                        <span className="text-sm text-gray-500">
                          {new Date(booking.start_time).toLocaleString()} –{" "}
                          {new Date(booking.end_time).toLocaleString()}
                        </span>
                      </div>
                      {booking.purpose && (
                        <p className="text-sm text-gray-700 mt-1">
                          {booking.purpose}
                        </p>
                      )}
                    </div>
                    <div className="flex gap-2 mt-2 sm:mt-0">
                      {(booking.status === "Upcoming" ||
                        booking.status === "Ongoing") && (
                        <>
                          <button
                            onClick={() => {
                              const newStart = prompt(
                                "New start (YYYY-MM-DD HH:MM):",
                                booking.start_time.slice(0, 16),
                              );
                              const newEnd = prompt(
                                "New end (YYYY-MM-DD HH:MM):",
                                booking.end_time.slice(0, 16),
                              );
                              if (newStart && newEnd)
                                handleReschedule(booking.id, newStart, newEnd);
                            }}
                            className="text-sm text-indigo-600 hover:underline"
                          >
                            Reschedule
                          </button>
                          <button
                            onClick={() => handleCancel(booking.id)}
                            className="text-sm text-red-600 hover:underline"
                          >
                            Cancel
                          </button>
                        </>
                      )}
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>
        </>
      )}
    </div>
  );
}
