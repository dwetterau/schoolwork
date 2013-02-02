daw2572, david.wetterau@gmail.com

To implement the depth first search I simply used recursion and a stack to store the moves needed to get to that point. This graph search algorithm is of course non optimal

To implement the BFS, I kept a map of point to path it took to get to that point to both keep track of which points I had been to and to be able to backtrack in O(1) time. As a slight memory improvement, I only stored in the map the path it took to get to the points along the fringe.

For the UCS and the A* algorithms I used the same backtracking method I talked about above but also kept separate sets for the nodes that I had expanded.

The state structure I used for the corners was a tuple of two tuples. The first was the location and the second was a 4 tuple of booleans that said whether or not I had been to a given corner.

The heuristic I used for the corners problem involved finding the manhatten distance to the closest point, then going from that point to the others greedily and adding the distance it took to each. This worked because you will never be able to do any better than a straight line path to any other corner once you are in a corner.

For my foodHeuristic, I constructed a minimum spanning tree of the food I hadn't been to yet and added up the distances of all of the edges in the MST using manhatten distance. After this I found the distance to the closest node from where I was and added this to the heuristic. Lastly, I found all the places that the MST intersected perpendicularly with walls in the maze and for each edge that intersected with a wall, I added an extra cost of 2 since you have to go around the wall. This passed all of the consistency and admissability checks and expanded just over 6000 nodes.

Question 8 involved changing two lines to see if there was food at a point X,Y in the goal check part of the AnyFoodAgent and invoking the breadth first search I had already written at the right time.

I spent a ton of time on the mini contest. My original solution was to find the closest point greedily and then find the closest after that to a certain depth and choose the food that had the lowest cost to go to next. I found that this left a lot of single points though so I added an extra case to check and see if the cost to the first node was about the same as the cost to get to all the other nodes and if this was the case it chose that one. I used two weights for this and I brute forced all of the combinations to find on a recursive depth of 3 to check and a factor of 4. 

I wasn't very happy with this solution though so I tried some other stuff. I read about a 2-opt exchange technique for slightly optimizing a travelling salesman problem and implemented it however it was sort of slow and wasn't better than my original recursive depth check. I left the code in however, I just commented out. The idea behind it was to greedily make a graph where food are nodes and always go to the closest non-visited one. After doing this you check every pair of edges and swap their destinations. If the new cost is less you keep the change. It was cool but didn't work all that well.
