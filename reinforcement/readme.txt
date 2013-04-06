Question 1. For this question we chose to do all of the value iteration and Q value iteration when the initialize method was called. We followed the exact formulas given in the book with the few modifications that were necessary because of the reward function. The code should be very self explanatory. This also meant that all calls for utilities or Q-values merely had to read from a dictionary that was guaranteed to have all of them.

Question 2. Our solution for the BridgeGrid simply involved setting the noise to 0.

Question 3. 
    To prefer the close exit but risk the bridge, we made the cost of living pretty bad (-3).
    To prefer the close exit but not risk the bridge, we made the noise higher and still had a pretty high cost of living
    To prefer the distant exit risking the cliff, we lowered the noise and had a sort of mad cost of living.
    To prefer the distant exit and avoid the cliff, we made the penalty of living 0
    To avoid all terminal states, we made the cost of living positive

Question 4. The Q-learning took the same form as the Q-Value iteration we did for the first problem. We initialized a Counter object to store the values and then computed them as we went. We followed the formulas in the book. We used the random.choice function to break ties to decide where to go.

Question 5. For this all we had to do was to use the flipCoin method and if it was true we randomly chose an action, otherwise we used the policy that we had already.

Question 6. This is not possible because if you increase the learning rate, you will want to go to the first good terminal state you find and if you lower it, you won't remember enough to get to the optimal exit. Even with a very lucky run with a high epsilon, in order for the optimal state to be propogated back as the q action to take would take more lucky runs to bring the value back.

Question 7. This worked with no modifications and we really cool or something.

Question 8. After around 1100 the reward started being positivie and he won 10/10 times.

Question 9. In order to implement this we had to be careful about the calling of the getQValue method which originally caused problems. After we fixed this and implemented the equation given in the lab handout we were done.
