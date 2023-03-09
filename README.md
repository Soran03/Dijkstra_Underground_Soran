# Dijkstra_Underground_Soran

A journey time calculator for the London Underground Map using Dijkstra's Algorithm

This project is something I did as a University project. I researched the different pathfinding algorithms such as A* and Dijkstra's algortihm
and decided on using the latter.

I have integrated the algorithm using a Microsoft Excel spreadsheet with contains most of the London underground and each station on those lines.
I converted the stations to a map in python, by using the dictionary data type, and had each station represtented as a node connected to all the other 
nodes (stations) and gave each connection weight which represents the time taken to reach that station.

When you run the code you are prompted to input your beginning and destination station.
The program will then run dijkstra's algorithm on the nap and return the shortest path for your inputs.
It will return each station and the time taken for your journey.
