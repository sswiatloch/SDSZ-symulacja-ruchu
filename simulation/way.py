import geopy.distance

from simulation.node import Node, TraversableNode
from simulation.range import Range
from typing import List


class Way:
    def __init__(self, way_id: int, begin_node: TraversableNode, end_node: TraversableNode,
                 intermediate_nodes: List[Node]):
        self.way_id = way_id
        self.begin_node = begin_node
        self.end_node = end_node
        self.intermediate_nodes = intermediate_nodes
        self.distance = 0
        self.ranges = []
        self.instantiate_nodes()

    def instantiate_nodes(self):
        previous_node = self.begin_node
        for intermediate_node in self.intermediate_nodes:
            cords_1 = (previous_node.lat, previous_node.long)
            cords_2 = (intermediate_node.lat, intermediate_node.long)
            distance = geopy.distance.vincenty(cords_1, cords_2)
            self.ranges.append((Range(self.distance, distance), (previous_node, intermediate_node)))
            self.distance += distance
            previous_node = intermediate_node
        cords_1 = (previous_node.lat, previous_node.long)
        cords_2 = (self.end_node.lat, self.end_node.long)
        distance = geopy.distance.vincenty(cords_1, cords_2).m
        self.ranges.append((Range(self.distance, distance), (previous_node, self.end_node)))
        self.distance += distance

    def coords_of_distance(self, distance: int):
        if distance > self.distance:
            print(f"Way {self.way_id} has only distance {self.distance}. I can't find coords of distance {distance}")
        else:
            range_nodepair = next(x for x in self.ranges if (x[0].__contains__(distance)))
            range = range_nodepair[0]
            percent_of_distance = (distance - range.start) / range.len()
            start_node = range_nodepair[1][0]
            end_node = range_nodepair[1][1]
            lat = (start_node.lat + ((end_node.lat - start_node.lat) * percent_of_distance))
            long = (start_node.long + ((end_node.long - start_node.long) * percent_of_distance))
            return lat, long