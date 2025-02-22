export interface ItineraryPreferences {
    destination: string;
    startDate: Date;
    endDate: Date;
    budget: {
        amount: number;
        type: 'per_day' | 'total';
    };
    interests: string[];
    dietaryRestrictions: string[];
    accommodationType: 'budget' | 'mid_range' | 'luxury';
    transportationType: 'public' | 'private' | 'walking';
}

export interface ItineraryResponse {
    id: string;
    query: string;
    itinerary_response: string;
    created_at: string;
    updated_at: string;
}

export interface ApiError {
    detail: string;
}
