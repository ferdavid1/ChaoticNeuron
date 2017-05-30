import numpy as np
import matplotlib.pyplot as plt
mu, sigma = 0, 1
poisson_random_dev = np.random.poisson(1, 1000)
plt.figure()
plt.hist(poisson_random_dev)
plt.show()