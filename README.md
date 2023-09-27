# Lets not wait!
> Winner of [Inrix Hack 2022](https://devpost.com/software/lets-not-wait)  
> Youtube video showcasing the app: [click here](https://youtu.be/kEpfnBIKG14?si=ZQlWvUgrg_ONtGaK)
>   

> ![Screenshot of app](https://d112y698adiu2z.cloudfront.net/photos/production/software_photos/002/294/049/datas/gallery.jpg)  
> Screenshot of the app

## Inspiration
> Often times we find the gas station that's closest to us and realize we have to wait in a long queue. Why not find the one which is closer but also has less wait time?

## What it does
> Based on the area or the location you enter, we find out which gas stations are in the vicinity. Not just that, we also show you the time you might spend in the queue to fill the gas along with some basic details like the address, name and contact details.

## How we built it
> With the help of the INRIX Fuel Station API, we got the data of the gas station in San Fransisco. Then for each gas station we calculated the waiting time. This was done with the help of INRIX's Trade Area Analytics API and data manipulations. We built an minimalistic UI to display the data of nearby gas station on Google Maps API.

## Challenges we ran into
1. No real time data available for fuel station. We had to fetch the data and keep it at our database.
2. No API (3rd Party or INRIX) available easily to get the waiting time of a vehicle. We calculated the waiting time using INRIX Trade Area Analytics API's startDateTime and endDateTime parameter.
3. We had the locations of the gas stations. But how do we find the nearest ones?
4. Discrepancy in the data. We had to do data cleaning and processing.

## Accomplishments that we're proud of
> We were successfully able to compute the wait time for gas station. Provide wait time to the user which will help save valuable time.

## What we learned
- Calling and understanding python flask REST API with tokens.
- Data cleaning & manipulations.
- Using Google maps API.
- Value extraction from data.

## What's next for Lets not wait!
> The accuracy of the waiting time can be improved with better data processing and machine learning. This waiting time can be integrated with routes to show the total time in reaching and filling the fuel.

## Built With
`css`
`database`
`flask`
`fuelstationapi`
`google-maps`
`html`
`javascript`
`pandas`
`python`
`tradeareaanalytics`















