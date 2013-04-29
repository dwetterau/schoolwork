david       daw2572   David Wetterau
jmslocum    jms6879   Josh Slocum

Agent name/folder/factory: DJ

Our agent is an agent that simply evaluates successor states in a smart way. We started our implementation by using the noisy sensor data to estimate the location of all enemy agents. We then combine this with actual location information if we ever get close enough to see them. We made this belief distribution in a way very similar to the tracking lab. After this our basic intuition was to have one agent attack intelligently and another defend. Our attacking agent considers many things, most importantly eating the food. He will also eat ghosts if he happens to eat the capsule. He values staying alive but if he's trapped or gets stuck, he will kill himself for the opportunity to try again. The intuition behind our defender was quite simple, never ever turn into a pacman, and get close to the enemy. If there is no enemy pacman, our ghost tracks the ghosts on the otherside to be ready when it comes over to our side. If instead there is a pacman, he will try to capture it. If he manages to be stuck right next to the pacman, he holds position until such a time that it's important to eat him so he can defend against a potential second attacker. 

This was the basic intuition behind our agent. We qualified on the 26th by tying with the staff agent in the rankings and then improved to rank 2. The next day we moved down to rank 3.
