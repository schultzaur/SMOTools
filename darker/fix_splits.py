errors = [
    ("All warp painting locations in all kingdoms", "Found with Sand Kingdom Art"),
    ("Found with Sand Kingdom Art", "Jammin' in the Sand Kingdom"),
    ("Jammin' in the Sand Kingdom", "Hat-and-Seek: In the Sand"),
    ("Hat-and-Seek: In the Sand", "Sand Kingdom Regular Cup"),
    ("Sand Kingdom Regular Cup", "Binding Band Returned"),
    ("Binding Band Returned", "Round-the-World Tourist"),
    ("Round-the-World Tourist", "Peach in the Sand Kingdom"),
    ("Peach in the Sand Kingdom", "Mighty Leap from the Palm Tree!"),
    ("Mighty Leap from the Palm Tree!", "On the North Pillar"),
    ("On the North Pillar", "Into the Flowing Sands"),
    ("Into the Flowing Sands", "In the Skies Above the Canyon"),
    ("In the Skies Above the Canyon", "Island in the Poison Swamp"),
    ("Island in the Poison Swamp", "An invisible Gleam"),
    ("An invisible Gleam", "On the Eastern Pillar"),
    ("On the Eastern Pillar", "Caught Hopping in the Desert!"),
    ("Caught Hopping in the Desert!", "Poster Cleanup"),
    ("Poster Cleanup", "Taking Notes: Running Down"),
    ("Taking Notes: Running Down", "Taking Notes: In the Wall Painting"),
    ("Taking Notes: In the Wall Painting", "Love at the Edge of the Desert"),
    ("Love at the Edge of the Desert", "More Walking in the Desert"),
    ("More Walking in the Desert", "Sand Kingdom Master Cup"),
    ("Sand Kingdom Master Cup", "Where the Transparent Platforms End"),
    ("Where the Transparent Platforms End", "Jump Onto the Transparent Lift"),
    ("Jump Onto the Transparent Lift", "Colossal Ruins: Dash Jump!"),
    ("Colossal Ruins: Dash Jump! and Sinking Colossal Ruins: Hurry!", "Sinking Colossal Ruins: Hurry!"),
    ("Through the Freezing Waterway", "Through the Freezing Waterway"),
    ("Freezing Waterway: Hidden Room", "Freezing Waterway: Hidden Room"),
]

for filename in ["Darker_Bayleef_3-11-47",]:
    with open(f"./darker/runs/{filename}.tsv", "r") as in_file:
        with open(f"./darker/runs/{filename}_fixed.tsv", "w") as out_file:
            for line in in_file:
                for error in errors:
                    if line.find(error[0]) > 0:
                        line = line.replace(error[0], error[1])
                        break
                out_file.write(line)



