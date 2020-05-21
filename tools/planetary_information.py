#! /usr/bin/env python3

ATMOSPHERES = dict(
    [(2, "Corrosive"),
     (3, "Inert, useless for respiration."),
     (4, "Airless/Thin")] +
    [(n, "Breathable") for n in range(5, 10)] +
    [(10, "Thick, requires a pressure mask."),
     (11, "Invasive"),
     (12, "Corrosive & Invasive")])

TEMPERATURES = dict(
    [(2, "Frozen, surface locked in perpetual ice. Atmosphere frozen into solid oxygen and lakes of liquid helium."),
     (3, "Cold, surface dominated by glaciers and tundra.")] +
    [(n, "Variable Cold") for n in range(4, 6)] +
    [(n, "Temperate") for n in range(6, 9)] +
    [(n, "Variable Warm") for n in range(9, 11)] +
    [(11, "Warm, surface predominantly tropical/desert with hotter areas."),
     (12, "Burning, surface inhospitable to human life with vacc suit or equivalent.")])

BIOSPHERES = dict(
    [(2, "Remnant, only the wreckage of a ruined biosphere remains."),
     (3, "Microbial, litte more that microbial life and the occasional slime mold exists.")] +
    [(n, "No native biosphere present.") for n in range(3, 6)] +
    [(n, "Human-Miscible") for n in range(6, 9)] +
    [(n, "Immiscible") for n in range(9, 11)] +
    [(11, "Hybrid"),
     (12, "Engineered")])

POPULATIONS = dict(
    [(2, "Failed Colony"),
     (3, "Outpost, few hundred to few thousand inhabitants")] +
    [(n, "Fewer than a million inhabitants") for n in range(4, 6)] +
    [(n, "Several million inhabitants") for n in range(6, 9)] +
    [(n, "Hundreds of millions of inhabitants") for n in range(9, 11)] +
    [(11, "Billions of inhabitants"),
     (12, "Alien inhabitants")])

TECHLEVEL = dict(
    [(2, "0, Neolithic-level technology"),
     (3, "1, Medieval technology")] +
    [(n, "2, Early Industrial Age technology") for n in range(4, 6)] +
    [(n, "4, Modern postech") for n in range(6, 9)] +
    [(n, "3, Early 21st century equivalent technology") for n in range(9, 11)] +
    [(11, "4+, Postech with specialities"),
     (12, "5, Pretech with surviving infrastructure")])
