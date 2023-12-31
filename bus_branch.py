#import attest.topology.db # No DB connection
import node_breaker
import unprocessed
import click
import datetime
import sys


class BusBranchModel:

    """Bus-branch model based on the given node-breaker model. Starts
    processing upon initialziation

    Args:
        node_breaker: node-breaker model"""

    def __init__(self, node_breaker):
        self._node_breaker = node_breaker
        self._topological_nodes = _ordered_nodes(
            node_breaker.topological_nodes)

        admittance_matrix = _calculate_admittance_matrix(node_breaker)
        self._admittance_matrix = admittance_matrix

    @property
    def admittance_matrix(self):
        """Model admittance matrix"""
        return self._admittance_matrix

    @property
    def topological_nodes(self):
        """Topological nodes"""
        return self._topological_nodes


def _calculate_admittance_matrix(node_breaker):
    connectivity_inv = {}
    for k, terminals in node_breaker.connectivity_map.items():
        for terminal in terminals:
            connectivity_inv[terminal] = k

    node_count = len(node_breaker.topological_nodes)
    matrix = [[0] * node_count for _ in range(node_count)]
    nodes = [node for node, _
             in _ordered_nodes(node_breaker.topological_nodes)]
    processed_lines = set()
    for i, node_mrid in enumerate(nodes):
        for term_mrid in node_breaker.connectivity_map[node_mrid]:
            terminal = node_breaker.asset_map[term_mrid]

            line_seg_mrid = terminal['cim:Terminal.ConductingEquipment']
            line_seg = node_breaker.asset_map.get(line_seg_mrid)
            if not line_seg or line_seg['cimclass'] != 'cim:ACLineSegment':
                continue
            if line_seg_mrid in processed_lines:
                continue
            processed_lines.add(line_seg_mrid)

            x = (line_seg['cim:ACLineSegment.x']
                 or line_seg['cim:ACLineSegment.x0'])
            r = (line_seg['cim:ACLineSegment.r']
                 or line_seg['cim:ACLineSegment.r0'])
            gch = (line_seg['cim:ACLineSegment.gch']
                   or line_seg['cim:ACLineSegment.g0ch'])
            bch = (line_seg['cim:ACLineSegment.bch']
                   or line_seg['cim:ACLineSegment.b0ch'])
            denominator = r ** 2 + x ** 2
            if denominator == 0:
                continue
            admittance = complex(r / denominator, - x / denominator)
            shunt = complex(gch / 2, bch / 2)

            other_term_mrid = [t for t
                               in node_breaker.terminal_map[line_seg_mrid]
                               if t != term_mrid][0]
            other_node = connectivity_inv[other_term_mrid]
            j = nodes.index(other_node)

            matrix[i][j] = -admittance
            matrix[i][i] += admittance + shunt
    return matrix


def _ordered_nodes(topological_nodes):
    return sorted([[node_mrid, elements]
                   for node_mrid, elements in topological_nodes.items()])



if __name__ == '__main__':
    pass
