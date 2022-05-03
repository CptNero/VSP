from dataclasses import dataclass
from enum import Enum
import graphviz as pgv
import pandas as pd


class Station(str, Enum):
    STATION_1 = 'Vá.1'
    STATION_2 = 'Vá.2'


@dataclass(frozen=True)
class Trip:
    start: int
    end: int
    duration: int
    from_station: Station
    to_station: Station

    def __str__(self):
        return f'{self.start}->{self.end}; {self.from_station} -> {self.to_station}'


def check_conflict(trip, schedule):
    conflicts = []

    for s_trip in schedule:
        if (max(trip.start, s_trip.start) <= min(trip.end, s_trip.end)
                and trip.from_station == s_trip.from_station and trip.to_station == s_trip.to_station):
            conflicts.append(s_trip)

    return len(conflicts) != 0, conflicts


def main():
    trips = []
    df = pd.read_excel('Input_VSP.xlsx', sheet_name='Járatok')

    for index, row in df.iterrows():
        start = row[0]
        end = row[1]
        duration = end - start
        type = row[2].split('->')
        from_station = Station(type[0])
        to_station = Station(type[1])

        trips.append(Trip(start, end, duration, from_station, to_station))

    schedule = set()
    schedule_conflicts = set()

    G = pgv.Digraph(engine='dot', format='svg', graph_attr={
        'rankdir': 'LR',
    })

    for trip in trips:
        is_conflict, conflicts = check_conflict(trip, schedule)
        if is_conflict:
            [schedule_conflicts.add(_) for _ in conflicts]
            [G.edge(str(trip), str(_)) for _ in conflicts]
            continue
        schedule.add(trip)
        G.node(str(trip))

    G.view(cleanup=True, filename='schedule_graph')


# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    main()


