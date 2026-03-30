export interface User {
  id: number
  username: string
  email: string
}

export interface Trip {
  id: number
  title: string
  destination: string
  type: string
  startDate: string
  endDate: string
  userId: number
  averageRating?: number
}

export interface Activity {
  time: string
  name: string
  type: string
  description?: string
  estimatedCost?: number
}

export interface ItineraryDay {
  day: number
  date?: string
  activities: Activity[]
}

export interface Itinerary {
  tripId: number
  days: ItineraryDay[]
  totalBudget?: number
  currency?: string
}

export interface Rating {
  id: number
  tripId: number
  userId: number
  score: number
  comment?: string
}

export interface AuthResponse {
  token: string
  user: User
}
