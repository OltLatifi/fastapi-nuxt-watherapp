export type LocationCreate = {
    name: string;
    latitude: number;
    longitude: number;
}

export type Location = {
    id: number;
    name: string;
    latitude: number;
    longitude: number;
}

export type City = {
    id: number
    name: string
    country: string
    longitude: number
    latitude: number
}

export type Forecast = {
    dates: string
    weather_codes: string
    min_temps: string
    max_temps: string
}

export type LocationAndForecast = {
    location: Location,
    forecast: Forecast
}