import click
import unprocessed
import node_breaker
import bus_branch
import datetime
import sys


@click.command()
@click.option('--filename', help='json CIM model file name', required=True)
def main(filename):
    unprocessed = unprocessed.UnprocessedModel()
    json = open(filename).read() # read the json string

    # Create topological merge map
    topological_nodes, connectivity_map = node_breaker.merge_nodes(unprocessed)
    node_breaker = node_breaker.NodeBreakerModel(unprocessed,topological_nodes,connectivity_map)

    # Calculate admittance matrix
    matrix = bus_branch.calculate_admittance_matrix(node_breaker)
    
    # Get the bus branch model
    bus_branch_model = bus_branch.NodeBranchModel(node_breaker, matrix)
    
    # Print out the result
    print(bus_branch_model)


if __name__ == '__main__':
    sys.exit(main())
