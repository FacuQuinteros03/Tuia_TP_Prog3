from ..models.grid import Grid
from ..models.frontier import QueueFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class BreadthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Breadth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        # Initialize a node with the initial position
        node = Node("", grid.start,0,None,None)


        # Initialize the explored dictionary to be empty
        explored = {} 
        
        if node.state == grid.end:
            return Solution(node, explored)

        # Initialize the frontier with the initial node
        # In this example, the frontier is a queue
        frontier = QueueFrontier()
        frontier.add(node)

        # Add the node to the explored dictionary
        explored[node.state] = True
        
        while True:

            print("Primera parte")

            if frontier.is_empty():
                print("Frontera vacia")
                return NoSolution(explored)

            #Remover nodo de la frontera
            node = frontier.remove()

            successors = grid.get_neighbours(node.state)
            

            for action,state in successors.items():
                print("recorrido de actions")
                
                if state not in explored:
                    new_node =  Node("", state, node.cost + grid.get_cost(state), parent=node, action=action)

                    if new_node.state == grid.end:
                        # running = False
                        return Solution(new_node, explored)

                    explored[state] = True
                    frontier.add(new_node)

                    

