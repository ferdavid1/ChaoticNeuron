import numpy as np
import matplotlib.pyplot as plt
mu, sigma = 0, 1
gaussian_random_dev = np.random.normal(mu, sigma, 1000)
plt.figure()
plt.title('Gaussian Distribution')
plt.hist(gaussian_random_dev)
plt.savefig('Gaussian_dist.png')
