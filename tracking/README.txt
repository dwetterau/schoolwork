david - David Wetterau
jmslocum - Joshua Slocum

For the first exercise all we did was take the probability of the belief and multiply by the evidence distribution which for this part simply consisted of finding the probability of the sensor reading given the actual believed manahatten distance.

For the second exercise we made a new game state for each legal position, put the ghost there and found the distribution of that ghost's successor states. We then multiplied this distribution by the old probability of the source location and added this accross all of the estimations. At the end we simply normalized our distribution.

For the third exercise we called our methods to updat ethe belif states and then greedily chose the action that minimized our distance to the most likely belief state. We interpretted this to be simply the location with the highest probability as opposed to something like a average middle position.

For the particle filtering we used the algorithms for particle filtering from the book. We initially used the uniform distribution of particles. Next we propogated each of the particles according to the tradition model in the same way we did the placing of the ghosts and getting their distributions earlier. Next we used the observe method and in this we updated the distribution of all particles by weighting the probability of the current particles according to the evidence and then we resampled our distribution.

For the joint particle filtering, we first updated the particles based off of the transition model. We did this by placing all the ghosts and moving their respective particles to a sampling of their movement distribution. We were able to reproduce a situation similar to the provided picture before we implemented the 6th exercise.

For the last exercise we had to use the evidence distributions to update the overall distribution. We did this by first calling the getBeliefDistribution method to get the current distribution, and updated the probabilities according to all of the evidence. In addition we handled the special case of already having eaten a ghost by looking through our measurements to find 999 distances, and then updating our distribution so that all of the keys would reflect that ghost in his prison location. To account for the other case, we went through our updated distribution at the end and if it was all 0, we resampled uniformly, otherwise we resampled the particles from the updated distribution.
