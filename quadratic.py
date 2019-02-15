#http://inversionlabs.com/2016/03/21/best-fit-surfaces-for-3-dimensional-data.html

import numpy as np
import scipy.linalg
from mpl_toolkits.mplot3d import Axes3D
import matplotlib.pyplot as plt

def slope_curvature(dem, res, window_size):
 
  #Define X and Y window datasets
  x = np.ones([window_size, window_size])
  for i in range(x.shape[0]):
    x[i:,] = (i+1)*res - res/2
  X = x.flatten() 
 
  y = np.ones([window_size, window_size])
  for j in range(y.shape[1]):
    y[:,j] = (j+1)*res - res/2
  Y = y.flatten() 

  #Define Central x and y coordinates
  center = int((window_size+1)/2)-1
  central_x = x[center, center]
  central_y = y[center, center]
 
  output_size = (
    (dem.shape[0] - window_size + 1), 
    (dem.shape[1] - window_size + 1))
   
  dem_slope = np.ones(dem.shape)
  dem_profile = np.ones(dem.shape)
  dem_plan = np.ones(dem.shape)
  dem_tangential = np.ones(dem.shape)
  
  i = 0
  j = 0
  for i in range(output_size[0]):
    print(i)
    output_i = int(i + ((window_size+1) / 2) - 1)
    for j in range(output_size[1]):
      window = dem[i:(i + window_size), j:(j + window_size)]
      C = fit(window, X, Y)
      slope, profile, plan, tangential = calculate(C, central_x, central_y)

      output_j = int(j + ((window_size+1) / 2) - 1)
      
      #write indices
      dem_slope[output_i, output_j] = slope
      dem_profile[output_i, output_j] = profile
      dem_plan[output_i, output_j] = plan
      dem_tangential[output_i, output_j] = tangential
      

  return dem_slope, dem_profile, dem_plan, dem_tangential 
 
def fit(z, X, Y):
  
  #format data 
  Z = z.flatten()
  data = np.c_[X, Y, Z]

  #best-fit quadratic curve (second order)
  A = np.c_[np.ones(data.shape[0]), data[:,:2], np.prod(data[:,:2], axis=1), data[:,:2]**2]
  C,_,_,_ = scipy.linalg.lstsq(A, data[:,2])

  #evaluate it on a grid
  #calcZ = np.dot(np.c_[np.ones(Z.shape), X, Y, X*Y, X**2, Y**2], C).reshape(z.shape)
  #x = X.reshape(z.shape)
  #y = Y.reshape(z.shape)

  #plot points and fitted surface with Matplotlib
  #fig1 = plt.figure(figsize=(10,10))
  #ax = fig1.gca(projection='3d')
  #ax.plot_surface(x, y, calcZ, rstride=1, cstride=1, alpha=0.2)
  #ax.scatter(data[:,0], data[:,1], data[:,2], c='r', s=50)
  #plt.xlabel('X')
  #plt.ylabel('Y')
  #ax.set_zlabel('Z')
  #ax.axis('equal')
  #ax.axis('tight')
  #plt.show()

  return C

def calculate(C, x, y):

  #Calculate Derivatives
  first_x = C[1] + C[3]*y + 2*C[4]*x
  first_y = C[2] + C[3]*y + 2*C[5]*x
  second_x = 2*C[4]
  second_y = 2*C[5]
  second_xy = C[3]

  #Calculate Terrain Indices
  p = (first_x)**2 + (first_y)**2

  slope = p**0.5

  profile = ((second_x*(first_x**2)) + (2*second_xy*first_x*first_y) + (second_y*(first_y**2))) / (p*((1+p)**(3/2)))

  plan = ((second_x*(first_x**2)) - (2*second_xy*first_x*first_y) + (second_y*(first_y**2))) / (p**(3/2))
  
  tangential = ((second_x*(first_x**2)) - (2*second_xy*first_x*first_y) + (second_y*(first_y**2))) / (p*((1+p)**(1/2)))

  return slope, profile, plan, tangential


