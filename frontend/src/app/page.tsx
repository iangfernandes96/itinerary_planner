'use client';

import { ItineraryDisplay } from '@/components/ItineraryDisplay';
import { ItineraryForm } from '@/components/ItineraryForm';
import { differenceInDays } from 'date-fns';
import { useState } from 'react';

export default function Home() {
  const [isLoading, setIsLoading] = useState(false);
  const [itinerary, setItinerary] = useState<any>(null);
  const [error, setError] = useState<string | null>(null);

  const handleSubmit = async (data: any) => {
    setIsLoading(true);
    setError(null);

    const duration = differenceInDays(data.endDate, data.startDate) + 1;

    try {
      const response = await fetch('http://localhost:8000/itinerary', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        // body: JSON.stringify({
        //   query: {
        //     location: data.location,
        //     duration,
        //     budget: Number(data.budget),
        //     accommodation: data.accommodation,
        //     transportation: data.transportation,
        //   }
        // }),
        body: JSON.stringify({
          query: 'Plan a ' + duration + '-day trip to ' + data.location + ' for a first-time visitor interested in culture and food. \
          Include sights to see, and restaurants to visit, with a total budget of ' + Number(data.budget) + ' Euros per day. \
          Also add options for ' + data.accommodation + ' type of accommodation, as well as options for ' + data.transportation + 'mode of transport.'
        })
      });

      if (!response.ok) {
        throw new Error('Failed to generate itinerary');
      }

      const result = await response.json();
      setItinerary(result.itinerary_response);
    } catch (err) {
      setError(err instanceof Error ? err.message : 'An error occurred');
    } finally {
      setIsLoading(false);
    }
  };

  return (
    <main className="container mx-auto py-8 px-4 min-h-screen bg-background">
      <h1 className="text-4xl font-bold text-center mb-8">
        Travel Itinerary Planner
      </h1>

      <div className="max-w-2xl mx-auto">
        <ItineraryForm onSubmit={handleSubmit} isLoading={isLoading} />

        {error && (
          <div className="mt-4 p-4 bg-destructive/10 text-destructive rounded-md">
            {error}
          </div>
        )}

        {itinerary && <ItineraryDisplay itinerary={itinerary} />}
      </div>
    </main>
  );
}
