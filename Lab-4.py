 import numpy as np, random, math
 def energy(state, image_size):
 mismatch = 0
 for i in range(image_size- 1):
 for j in range(image_size- 1):
 mismatch += np.sum(np.abs(state[i][j+1]- state[i][j])) # Horizontal
 mismatch += np.sum(np.abs(state[i+1][j]- state[i][j])) # Vertical
 return mismatch
 def simulated_annealing(state, T=1000, alpha=0.98, max_iter=5000):
 current_state = np.copy(state)
 best_state = np.copy(state)
 current_energy = energy(current_state, len(state))
 best_energy = current_energy
for _ i
 i1, j1, i2, j2 = np.random.randint(0, len(state), 4)
 neighbor = np.copy(current_state)
 neighbor[i1][j1], neighbor[i2][j2] = neighbor[i2][j2], neighbor[i1][j1]
 new_energy = energy(neighbor, len(state))
 delta_E = new_energy- current_energy
 if delta_E < 0 or random.random() < math.exp(-delta_E / T):
 current_state, current_energy = neighbor, new_energy
 if new_energy < best_energy:
 best_state, best_energy = neighbor, new_energy
 T *= alpha
 if T < 1e-3:
 break
 return best_state, best_energy
