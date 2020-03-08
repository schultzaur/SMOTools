from enum import Enum
from route import ROUTE
import csv

class Runners(str, Enum):
    DANGERS = "Dangers"
    NEO =     "Neo"
    VALLU =   "Vallu"
    BAYLEEF = "Bayleef"
    CHAOS =   "Chaos"
    NICRO =   "Nicro"
    TIMPANI = "Timpani"
    KERBIS =  "Kerbis"
    FIR =     "Fir"

class SourceType(Enum):
    YouTube = 0
    Twitch = 1

class Source(object):
    def __init__(self, sourceType, id):
        self.type = sourceType
        self.id = id

class Run(object):
    def __init__(self, runner, splits_file, source):
        self.runner = runner
        self.splits_file = splits_file
        self.source = source
    def readSubSplits(self):
        subsplits = []
        
        try:
            with open(f"./darker/runs/{self.splits_file}.tsv", "r") as file:
                last_time =  None
                last_moon = None
                for row in csv.reader(file, delimiter='\t'):
                    time = float(row[0])
                    moon = row[1].strip()

                    if last_moon:
                        print(moon, last_moon)
                        subsplits.append(Subsplit(last_moon, moon, last_time, time))
                    
                    last_time = time
                    last_moon = moon
        except FileNotFoundError:
            print(f"{self.splits_file} missing.")
        return subsplits


RUNS = {
    Runners.DANGERS: [
        Run(Runners.DANGERS, "Darker_Dangers_3-08-25", Source(SourceType.YouTube, "DzJQplLyiZQ")),
        Run(Runners.DANGERS, "Darker_Dangers_3-08-34", Source(SourceType.YouTube, "6cfw9V1628w")),
        Run(Runners.DANGERS, "Darker_Dangers_3-09-03", Source(SourceType.YouTube, "_A0Dh3gnI-M")),
        Run(Runners.DANGERS, "Darker_Dangers_3-09-50", Source(SourceType.YouTube, "0usPoO9suGA")),
    ],
    Runners.NEO: [
        Run(Runners.NEO, "Darker_Neo_3-10-45", Source(SourceType.YouTube, "nYINBviIDHc")),
        Run(Runners.NEO, "Darker_Neo_3-11-08", Source(SourceType.YouTube, "6Odz5Dk9teI")),
        Run(Runners.NEO, "Darker_Neo_3-11-58", Source(SourceType.YouTube, "AhO0jPiSTVA")),
    ],
    Runners.VALLU: [
        Run(Runners.VALLU, "Darker_Vallu_3-11-29", Source(SourceType.Twitch, "552750629")),
        Run(Runners.VALLU, "Darker_Vallu_3-14-12", Source(SourceType.Twitch, "549553023")),
        Run(Runners.VALLU, "Darker_Vallu_3-15-19", Source(SourceType.Twitch, "545566422")),
    ],
    Runners.BAYLEEF: [
        Run(Runners.BAYLEEF, "Darker_Bayleef_3-11-47", Source(SourceType.YouTube, "_GOKUjaQqkE")),
        Run(Runners.BAYLEEF, "Darker_Bayleef_3-13-13", Source(SourceType.Twitch, "545566422")),

    ],
    Runners.CHAOS: [
        Run(Runners.CHAOS, "Darker_Chaos_3-12-54", Source(SourceType.YouTube, "JOhb1JrZnls")),
        Run(Runners.CHAOS, "Darker_Chaos_3-14-23", Source(SourceType.YouTube, "VAKdNxYsKDU")),
    ],
    Runners.NICRO: [
        Run(Runners.NICRO, "Darker_Nicro_3-14-43", Source(SourceType.Twitch, "422388232")),
    ],
    Runners.TIMPANI: [
        Run(Runners.TIMPANI, "Darker_Timpani_3-14-47", Source(SourceType.YouTube, "RdHnTX5fnMY")),
    ],
    Runners.KERBIS: [
        Run(Runners.KERBIS, "Darker_Kerbis_3-15-21",  Source(SourceType.Twitch,  "441136071")),
    ],
    Runners.FIR: [
        Run(Runners.FIR, "Darker_Fir 3-15-28", Source(SourceType.Twitch,  "493692509")),
    ],
}

class Clip(object):
    def __init__(self, source, start, end):
        self.source = source
        self.start = start
        self.end = end
    def url(self):
        if self.source.type == SourceType.YouTube:
            return "https://www.youtube.com/embed/{0}?start={1}&end={2}".format(
                self.source.id,
                round(self.start - .5),
                round(self.end + .5))
        elif self.source.type  == SourceType.Twitch:
            return "https://player.twitch.tv/?video={0}&autoplay=false&time={1}s".format(
                self.source.id,
                round(self.start - .5))
        return None

class Subsplit(object):
    def __init__(self, start_moon, end_moon, start_time, end_time):
        self.start_moon = start_moon
        self.end_moon = end_moon
        self.start_time = start_time
        self.end_time = end_time
        self.key = (self.start_moon, self.end_moon)
        self.duration = self.end_time - self.start_time

def get_clips(runners, best_by_runner, subsplit, subsplit_id):
    clips = []
    for runner in runners:
        clip_id = subsplit_id + "-" + runner.value
        if subsplit in best_by_runner[runner]:
            clip = best_by_runner[runner][subsplit]
            clips.append({
                "id": clip_id,
                "time": clip.end - clip.start,
                "url": clip.url()
            })
        else:
            clips.append({
                "id": clip_id,
                "time": None,
                "url": None
            })
    return clips

if __name__ == "__main__":
    import json
    output = {
        "runners": [],
        "splits": []
    }

    best_by_runner = {}

    runners = []
    for runner, runs in RUNS.items():
        runners.append(runner)
        best_clips = {}
        best_by_runner[runner] = best_clips
        for run in runs:
            for subsplit in run.readSubSplits():
                if subsplit.key not in best_clips or subsplit.duration < best_clips.duration:
                    best_clips[subsplit.key] = Clip(run.source, subsplit.start_time, subsplit.end_time)


    for split_name, subsplits in ROUTE.items():
        split_id = split_name.replace(" ","").lower()
        split = {
            "id": split_id,
            "name": split_name,
            "subsplits": []
        }
        for i, subsplit in enumerate(subsplits):
            subsplit_id = split_id + "-" + str(i)
            clips = get_clips(runners, best_by_runner, subsplit, subsplit_id)
         
            split["subsplits"].append({
                "id": subsplit_id,
                "from": subsplit[0],
                "to": subsplit[1],
                "clips": clips
            })
        output["splits"].append(split)

    with open("./darker/runs/aggregate.json", 'w') as out:
        json.dump(output, out, indent=1)