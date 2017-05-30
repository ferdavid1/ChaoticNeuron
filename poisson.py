import numpy as np
import matplotlib.pyplot as plt

poisson_random_dev = np.random.poisson(1, 1000)
plt.figure()
plt.hist(poisson_random_dev)
plt.show()