'use client';

import { Card, CardContent } from '@/components/ui/card';
import ReactMarkdown from 'react-markdown';

interface ItineraryDisplayProps {
    itinerary: string;
}

export function ItineraryDisplay({ itinerary }: ItineraryDisplayProps) {
    return (
        <Card className="w-full">
            <CardContent className="p-6">
                <div className="prose prose-neutral dark:prose-invert max-w-none">
                    <ReactMarkdown>{itinerary}</ReactMarkdown>
                </div>
            </CardContent>
        </Card>
    );
}
