from excel_data_processor import *

underground_data = "London Underground data.xlsx"


def main():
    shortest_path_algorithm()


def dijkstra_shortest_path(underground_map, start, target):
    stn_path = []
    previous = {start: None}
    travel_time = {start: 0}

    while len(stn_path) <= len(underground_map):
        stn_path.append(start)

        for linked_stns in underground_map[start]:
            linked_stn = linked_stns["station"]

            if linked_stn in stn_path:
                continue
            else:
                temp_travel_time = travel_time[start] + linked_stns["time"]

                if linked_stn in travel_time:
                    if temp_travel_time < travel_time[linked_stn]:
                        travel_time[linked_stn] = temp_travel_time
                        previous[linked_stn] = start
                else:
                    travel_time[linked_stn] = temp_travel_time
                    previous[linked_stn] = start

        min_time = float('inf')
        for station in travel_time:
            if station not in stn_path and travel_time[station] < min_time:
                min_time = travel_time[station]
                start = station

    path = []
    if True:
        next_stn = target

        while next_stn is not None:
            path.append(next_stn)
            next_stn = previous[next_stn]

        path.reverse()

    return path, travel_time[target]


def shortest_path_algorithm():
    tube_lines_table, routes_table = get_data_from_excel(underground_data)
    tube_map: TubeMap = get_tube_map_graph(tube_lines_table, routes_table)

    start_input = input("Where will you begin: ").title().strip()
    end_input = input("Where will you end: ").title().strip()

    while not (start_input in tube_map and end_input in tube_map):
        if start_input not in tube_map:
            start_input = input("Beginning station not valid, try again: ")
            continue
        if end_input not in tube_map:
            end_input = input("Ending station not valid, try again: ")

    output = dijkstra_shortest_path(tube_map, start_input, end_input)

    print_route(output)


def print_route(output):
    print("\n"
          "The journey path is: "
          "\n")
    for x in range(len(output[0])):
        print(output[0][x])

    print("\n"
          "The travel time is: " +
          str(output[1]) +
          " minutes")


if __name__ == "__main__":
    main()
