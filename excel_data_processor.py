from pandas import read_excel, concat, DataFrame, Series
from typing import Any, Dict, List, Set, Tuple, TypeAlias

Station: TypeAlias = str
TubeMap: TypeAlias = Dict[Station, List[Dict[str, Any]]]


def get_data_from_excel(file_name: str) -> Tuple[DataFrame, DataFrame]:
    ''''''
    tube_data: DataFrame = read_excel(file_name)
    columns: List[str] = list(tube_data.columns)
    tube_data[columns[1]] = tube_data[columns[1]].map(lambda s: s.strip() if type(s) == str else s)
    tube_data[columns[2]] = tube_data[columns[2]].map(lambda s: s.strip() if type(s) == str else s)

    tube_lines_table: DataFrame = tube_data[tube_data[columns[2]].isna() & tube_data[columns[3]].isna()].drop(
        columns[2:], axis=1)
    routes_table: DataFrame = tube_data[~tube_data[columns[2]].isna() | ~tube_data[columns[3]].isna()]
    return tube_lines_table, routes_table


def create_empty_tube_map(tube_lines_table: DataFrame) -> TubeMap:
    return dict((station, []) for _, (_, station) in tube_lines_table.iterrows())


def get_tube_map_graph(tube_lines_table: DataFrame, routes_table: DataFrame) -> TubeMap:
    tube_map: TubeMap = create_empty_tube_map(tube_lines_table)

    for _, row in routes_table.iterrows():
        line, station1, station2, time = row
        tube_map[station1].append({"station": station2, "line": line, "time": int(time)})
        tube_map[station2].append({"station": station1, "line": line, "time": int(time)})

    return tube_map


def get_min_tube_map_graph(tube_lines_table: DataFrame, routes_table: DataFrame) -> Tuple[TubeMap, DataFrame]:
    columns: List[str] = list(routes_table.columns)
    routes_table_ordered = routes_table.sort_values(by=[columns[3], columns[0]])

    start: Station = tube_lines_table.iloc[0, 1]
    min_tube_map: TubeMap = create_empty_tube_map(tube_lines_table)
    routes_to_remove: DataFrame = DataFrame(columns=columns)
    for _, row in routes_table_ordered.iterrows():
        line, station1, station2, time = row
        if does_route_exist(min_tube_map, station1, station2):
            routes_to_remove.loc[len(routes_to_remove)] = row
        else:
            min_tube_map[station1].append({"station": station2, "line": line, "time": int(time)})
            min_tube_map[station2].append({"station": station1, "line": line, "time": int(time)})
            if has_cycle(min_tube_map, start, dict((station, False) for station in min_tube_map.keys())):
                min_tube_map[station1].remove({"station": station2, "line": line, "time": int(time)})
                min_tube_map[station2].remove({"station": station1, "line": line, "time": int(time)})
                routes_to_remove.loc[len(routes_to_remove)] = row

    return min_tube_map, routes_to_remove


def does_route_exist(min_span_graph: TubeMap, station1: Station, station2: Station) -> bool:
    return any(route["station"] == station2 for route in min_span_graph[station1]) or \
           any(route["station"] == station1 for route in min_span_graph[station2])


def has_cycle(min_span_graph: TubeMap, current: Station, visited: Dict[Station, bool], previous: Station = None) -> bool:
    visited[current] = True
    for route in min_span_graph[current]:
        if not visited[route["station"]]:
            if has_cycle(min_span_graph, route["station"], visited, current):
                return True
        elif route["station"] != previous:
            return True
    return False


def print_tube_map(tube_map: TubeMap) -> str:
    for station in sorted(tube_map.keys()):
        output = f"{station}: ["
        for route in tube_map[station]:
            output += f"\n  {route},"
        output += "\n]"
        print(output)

