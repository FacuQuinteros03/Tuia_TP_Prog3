from ..models.grid import Grid
from ..models.frontier import StackFrontier
from ..models.solution import NoSolution, Solution
from ..models.node import Node


class DepthFirstSearch:
    @staticmethod
    def search(grid: Grid) -> Solution:
        """Find path between two points in a grid using Depth First Search

        Args:
            grid (Grid): Grid of points
            
        Returns:
            Solution: Solution found
        """
        node = Node("", grid.start,0,None,None)


        # Initialize the explored dictionary to be empty
        explored = {} 
        
        if node.state == grid.end:
            return Solution(node, explored)

        # Initialize the frontier with the initial node
        frontier = StackFrontier()
        frontier.add(node)
        while True:
            print("Primera parte")
            if frontier.is_empty():
                print("Frontera vacia")
                return NoSolution(explored)

            #Remover nodo de la frontera
            node = frontier.remove()
            
            #control que evita expandir un estado ya expandido
            if node.state in explored:
                continue    
            explored[node.state] = True
            
            successors = grid.get_neighbours(node.state)    

            for action,state in successors.items():
                print("recorrido de actions")
                    
                if state not in explored:
                    new_node =  Node("", state, node.cost + grid.get_cost(state), parent=node, action=action)

                    if new_node.state == grid.end:
                        return Solution(new_node, explored)

                    frontier.add(new_node)
