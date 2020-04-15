#! /usr/bin/env python3
import swn_database.data as swn_data

def populate_planets(planetList: list):
    planetList.append(swn_data.Planet(0, "Planet A", swn_data.Coordinate.From_Hex('B2')))
    planetList.append(swn_data.Planet(1, "Planet B", swn_data.Coordinate.From_Hex('B4')))
    planetList.append(swn_data.Planet(2, "Planet C", swn_data.Coordinate.From_Hex('A4')))
    planetList.append(swn_data.Planet(3, "Planet D", swn_data.Coordinate.From_Hex('A5')))

if __name__ == "__main__":
    CONNECTIONS = []
    PLANETS = []

    #print(swn_data.Coordinate(1,2))

    populate_planets(PLANETS)
    [print(planet) for planet in PLANETS]

    pass