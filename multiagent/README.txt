daw2572, david.wetterau@gmail.com
jms6879, jmslocum16@yahoo.com

Question 1: For this we just found the closest ghost and food and tried to maximize the furthest ghost and minimize the closest food. We did this by adding and subtracting their reciprocals and adding the current score of the board so that we wouldn't just sit still.

Question 2: We implemented minimax by making two nested functions that we called recursively. We called max first on the agent and then min on each subsequent ghost. After all ghosts, the last ghost would call max again on pacman with a depth 1 greater. Once we reached the target depth, we returned the evaluation function of the state.

Question 3: We modified our minimax implementation so that we would stop minimizing if we found a value less than the max we had passed in and we stopped maximizing if we were minimizing in the parent and had already found a smaller value than the current max. We were unable to prune for subsequent min-min calls for obvious reasons.

Question 4: We removed the alpha beta pruning since we were no longer finding true minimimums and then took the average of all the results for whenever we called the modified getMin function. This enabled pacman to make more risky moves since he assumed that the ghosts did not always behave optimally.

Question 5: For our better evaluation function, we used a combination of min ghost distance, max ghost distance, min food distance, max food distance, a score of ghost eatability, the number of food pellets left, and the current game score. The ghost eatability was the ratio of how far away it was and how much time was left to kill it. We also added a bonus for eating a ghost. The inclusion of the number of food left encouraged pacman to continue eating food. Once again adding the score of the game kept pacman from standing still because of the penalty for living.

Mini-contest: For the minicontest we used the same evaluation function that we made in Question 5. It sort of works okay. We tweaked a few of the weights on the parameters we were caring about but didn't change too much.
