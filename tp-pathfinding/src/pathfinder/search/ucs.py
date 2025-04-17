from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class UniformCostSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Uniform Cost Search

        Args:
            grid (Grid): Grid of points

        Returns:
            Solution: Solution found
        """
        
        # Initialize a node with the initial position
        node = Node("", grid.start,0,None,0)

        frontier = StackFrontier()

        frontier.add(node)

        # Add the node to the explored dictionary
        explored = {node.state: node.cost}
        
        while True:

            print("Primera parte")

            if frontier.is_empty():
                print("Frontera vacia")
                return NoSolution(explored)

            #Remover nodo de la frontera
            node = frontier.remove()
            
            if node.state == grid.end:
                return Solution(node, explored)

            successors = grid.get_neighbours(node.state)
            
            for action,state in successors.items():
                print("recorrido de actions")
                new_cost = node.cost + grid.get_cost(node.state) 
                new_node =  Node("", state, new_cost, parent=node, action=action)

                if state not in explored or new_cost < explored[new_node.state]:
                    
                    if new_node.state == grid.end:
                        # running = False
                        return Solution(new_node, explored)

                    explored[state] = new_node.cost
                    frontier.add(new_node)

