import sunny from "~/assets/1.svg"
import thunderStorm from "~/assets/2.svg"
import partlyCloudy from "~/assets/3.svg"
import cloudy from "~/assets/4.svg"
import rainy from "~/assets/5.svg"

const weatherMappings = [
    { codes: ['0', '1'], icon: sunny },
    { codes: ['2'], icon: partlyCloudy },
    { codes: ['3', '45', '48'], icon: cloudy },
    { codes: ['51', '53', '55', '56', '57', '61', '63', '80'], icon: rainy },
    { codes: ['65', '95', '96', '97', '98', '99'], icon: thunderStorm }
];

export const loadWeatherIcon = (weatherCode: string) => {
    const mapping = weatherMappings.find(({ codes }) => codes.includes(weatherCode));
    return mapping ? mapping.icon : sunny;
}