import { Container, LoadingOverlay, MantineProvider, Paper, Text } from '@mantine/core';
import { useState } from 'react';
import { ItineraryForm } from './components/ItineraryForm';
import { createItinerary } from './services/api';
import { ItineraryPreferences, ItineraryResponse } from './types/itinerary';

function App() {
  console.log('App component rendered'); // Debug line
  const [isLoading, setIsLoading] = useState(false);
  const [error, setError] = useState<string | null>(null);
  const [itinerary, setItinerary] = useState<ItineraryResponse | null>(null);

  const handleSubmit = async (preferences: ItineraryPreferences) => {
    console.log('Form submitted with preferences:', preferences); // Debug line
    setIsLoading(true);
    setError(null);
    try {
      const response = await createItinerary(preferences);
      console.log('Itinerary created successfully:', response); // Debug line
      setItinerary(response);
    } catch (err) {
      console.error('Error creating itinerary:', err); // Debug line
      setError(err instanceof Error ? err.message : 'Failed to generate itinerary');
    } finally {
      setIsLoading(false);
      console.log('Loading state set to false'); // Debug line
    }
  };

  return (
    <MantineProvider>
      <Container size="lg" py="xl">
        <Text>Debug: App is rendering...</Text> {/* Debug message */}
        <ItineraryForm onSubmit={handleSubmit} isLoading={isLoading} />

        {error && (
          <Paper p="md" mt="md" style={{ backgroundColor: '#fff4f4' }}>
            <Text color="red">{error}</Text>
          </Paper>
        )}

        {itinerary && (
          <Paper p="md" mt="md" withBorder>
            <LoadingOverlay visible={isLoading} />
            <Text size="sm" style={{ whiteSpace: 'pre-line' }}>
              {itinerary.itinerary_response}
            </Text>
          </Paper>
        )}
      </Container>
    </MantineProvider>
  );
}

export default App;
