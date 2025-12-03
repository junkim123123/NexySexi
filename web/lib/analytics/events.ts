export type Event = {
    type: string;
    timestamp: string;
    metadata?: Record<string, any>;
};

const MAX_EVENTS_PER_IDENTITY = 50;
const events = new Map<string, Event[]>();

export function addEvent(identity: string, event: Event) {
    if (!events.has(identity)) {
        events.set(identity, []);
    }
    const userEvents = events.get(identity)!;
    userEvents.push(event);
    if (userEvents.length > MAX_EVENTS_PER_IDENTITY) {
        userEvents.shift(); // Remove the oldest event
    }
    events.set(identity, userEvents);
}

export function getEvents(identity: string): Event[] {
    return events.get(identity) || [];
}