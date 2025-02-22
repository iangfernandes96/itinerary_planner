import axios from 'axios';
import { ItineraryPreferences, ItineraryResponse } from '../types/itinerary';

// When running in Docker, use the backend service name
// When running in development, use localhost
const apiUrl = window.location.hostname === 'localhost'
    ? 'http://localhost:8000'
    : import.meta.env.VITE_API_URL;

const api = axios.create({
    baseURL: apiUrl,
    headers: {
        'Content-Type': 'application/json',
    },
});

export async function createItinerary(preferences: ItineraryPreferences): Promise<ItineraryResponse> {
    // Convert preferences to a query string format that matches backend expectations
    const query = `Plan a trip to ${preferences.destination} from ${preferences.startDate.toLocaleDateString()} to ${preferences.endDate.toLocaleDateString()} with a ${preferences.budget.type} budget of ${preferences.budget.amount}. Interests include ${preferences.interests.join(', ')}. ${preferences.dietaryRestrictions.length ? `Dietary restrictions: ${preferences.dietaryRestrictions.join(', ')}.` : ''} Preferred accommodation type: ${preferences.accommodationType}. Preferred transportation: ${preferences.transportationType}.`;

    const response = await api.post<ItineraryResponse>('/itinerary/', {
        query,
    });

    return response.data;
}

export async function getItinerary(id: string): Promise<ItineraryResponse> {
    const response = await api.get<ItineraryResponse>(`/itinerary/${id}`);
    return response.data;
}
