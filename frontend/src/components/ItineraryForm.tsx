import {
    Button,
    Container,
    Group,
    Paper,
    Select,
    Stack,
    TextInput,
    Title,
    useMantineTheme
} from '@mantine/core';
import { DatePickerInput } from '@mantine/dates';
import { useForm } from '@mantine/form';
import { IconCalendar, IconPlane } from '@tabler/icons-react';
import { useEffect, useState } from 'react';
import { ItineraryPreferences } from '../types/itinerary';


const INTERESTS = [
    { value: 'historical', label: 'Historical Sites', group: 'Culture' },
    { value: 'cultural', label: 'Cultural Experiences', group: 'Culture' },
    { value: 'nature', label: 'Nature & Outdoors', group: 'Activities' },
    { value: 'food', label: 'Food & Dining', group: 'Food & Drink' },
    { value: 'shopping', label: 'Shopping', group: 'Activities' },
    { value: 'art', label: 'Art & Museums', group: 'Culture' },
    { value: 'nightlife', label: 'Nightlife', group: 'Entertainment' },
    { value: 'relaxation', label: 'Relaxation & Wellness', group: 'Activities' },
];

export function ItineraryForm({ onSubmit, isLoading }: { onSubmit: (values: ItineraryPreferences) => void; isLoading: boolean }) {
    console.log('ItineraryForm component rendered'); // Debug line
    const theme = useMantineTheme();
    const [budgetType, setBudgetType] = useState<'per_day' | 'total'>('total');

    const form = useForm<ItineraryPreferences>({
        initialValues: {
            destination: '',
            startDate: new Date(),
            endDate: new Date(new Date().setDate(new Date().getDate() + 7)),
            budget: {
                amount: 0,
                type: 'total',
            },
            interests: [],
            dietaryRestrictions: [],
            accommodationType: 'mid_range',
            transportationType: 'public',
        },
        validate: {
            destination: (value) => (!value ? 'Destination is required' : null),
            budget: {
                amount: (value) => (value <= 0 ? 'Budget must be greater than 0' : null),
            },
            // startDate: (value, values) =>
            //     new Date(value) >= new Date(values.endDate)
            //         ? 'Start date must be before end date'
            //         : null,
        },
    });

    const handleSubmit = form.onSubmit((values) => {
        console.log('Form values submitted:', values); // Debug line
        onSubmit({
            ...values,
            budget: {
                ...values.budget,
                type: budgetType,
            },
        });
    });

    useEffect(() => {
        console.log('ItineraryForm initial values:', form.values); // Debug line
    }, []);

    return (
        <Container size="md" py="xl">
            <Paper radius="md" p="xl" withBorder>
                <form onSubmit={handleSubmit}>
                    <Stack gap="lg">
                        <Group justify="space-between" align="baseline">
                            <Title order={2} fw={900} c={theme.primaryColor}>
                                Plan Your Dream Trip
                            </Title>
                            <IconPlane size={30} color={theme.colors[theme.primaryColor][6]} />
                        </Group>

                        <TextInput
                            label="Destination"
                            placeholder="Enter your destination"
                            {...form.getInputProps('destination')}
                        />

                        <DatePickerInput
                            icon={<IconCalendar size={16} />}
                            type="range"
                            label="Trip Duration"
                            placeholder="Select start and end dates"
                            value={[form.values.startDate, form.values.endDate]}
                            onChange={(dates) => {
                                if (dates) {
                                    form.setFieldValue('startDate', dates[0]);
                                    form.setFieldValue('endDate', dates[1]);
                                }
                            }}
                        />

                        {/* <div style={{ position: 'relative', zIndex: 1 }}>
                            <MultiSelect
                                label="Interests"
                                placeholder="Select your interests"
                                data={INTERESTS}
                                value={form.values.interests || []}
                                onChange={(values) => form.setFieldValue('interests', values)}
                                withinPortal
                            />
                        </div> */}

                        <TextInput
                            label="Budget Amount"
                            placeholder="Enter your budget"
                            {...form.getInputProps('budget.amount')}
                        />

                        <Select
                            label="Accommodation Type"
                            data={[
                                { value: 'budget', label: 'Budget' },
                                { value: 'mid_range', label: 'Mid Range' },
                                { value: 'luxury', label: 'Luxury' },
                            ]}
                            {...form.getInputProps('accommodationType')}
                        />

                        <Select
                            label="Transportation Type"
                            data={[
                                { value: 'public', label: 'Public' },
                                { value: 'private', label: 'Private' },
                                { value: 'walking', label: 'Walking' },
                            ]}
                            {...form.getInputProps('transportationType')}
                        />

                        <Button type="submit" loading={isLoading}>
                            Submit
                        </Button>
                    </Stack>
                </form>
            </Paper>
        </Container>
    );
}
