export interface Asset {
  id: number;
  asset_tag: string;
  name: string;
  category_id: number;
  serial_number?: string;
  status: string;
  department_id?: number;
  is_bookable: boolean;
}

export type BookingStatus = 'Upcoming' | 'Ongoing' | 'Completed' | 'Cancelled';

export interface Booking {
  id: number;
  asset_id: number;
  booked_by: number;
  start_time: string;  
  end_time: string;
  purpose: string | null;
  status: BookingStatus;
  created_at: string;
}