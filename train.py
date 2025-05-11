import signal
import sys
import plotly.graph_objects as go
from utils import *
import argparse


class LinearRegression:  
  def __init__(self, input, output, alpha, iteration, plot_result, plot_cost):
     
    #data
    self.data = get_data(input)
    self._x = self.data[0]
    self._y = self.data[1]
    self.x = normalize(self._x)
    self.y = normalize(self._y)

    #theta0 and theta1
    self._t0 = 0
    self._t1 = 0
    #normalize theta0 and theta1
    self.t0 = 0
    self.t1 = 0

    self.alpha = alpha
    self.max_iteration = iteration

    self.iteration = 0
    self.m = len(self.x)
    
    self.C = []
    
    self.b_plot_result = plot_result
    self.b_plot_cost = plot_cost
    
    self.output = output

  def cost(self):
    cost = 0
    self.unnormalize_thetas()
    
    for i in range(self.m):
      cost += (self._t0 + self._t1 * self._x[i] - self._y[i]) ** 2
      
    self.C.append((1 / (2 * self.m)) * cost)

  def gradient_descent(self):
    for _ in range(self.max_iteration):
      d0 = 0
      d1 = 0

      for i in range(self.m):
        error = (self.t0 + self.t1 * self.x[i]) - self.y[i]
        d0 += error
        d1 += error * self.x[i]

      self.t0 = self.t0 - self.alpha * (2 / self.m) * d0
      self.t1 = self.t1 - self.alpha * (2 / self.m) * d1

      self.cost()

      self.iteration += 1
      
  def unnormalize_thetas(self):
    x_min, x_max = min(self._x), max(self._x)
    y_min, y_max = min(self._y), max(self._y)

    scale_x = x_max - x_min
    scale_y = y_max - y_min

    self._t1 = self.t1 * scale_y / scale_x
    self._t0 = self.t0 * scale_y - self._t1 * x_min + y_min

  def plot_cost(self):
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(x=list(range(len(self.C))), y=self.C, mode='lines', name='Cost'))
    fig.update_layout(title='Cost evolution', 
                      xaxis_title='Iteration', 
                      yaxis_title='Cost')
    
    fig.show()

  def plot_result(self):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=self._x, y=self._y, mode='markers', name='Data'))
    
    x_min_data = min(self._x)
    x_max_data = max(self._x)
    x_range = x_max_data - x_min_data
    x_start = x_min_data - 0.2 * x_range
    x_end = x_max_data + 0.2 * x_range

    y_start = self._t0 + self._t1 * x_start
    y_end = self._t0 + self._t1 * x_end

    fig.add_trace(go.Scatter(
        x=[x_start, x_end],
        y=[y_start, y_end],
        mode='lines',
        name='Regression Line'
    ))
    fig.update_layout(title='Price vs. Kilometers',
                      xaxis_title='Kilometers',
                      yaxis_title='Price')
    fig.show()

  def print_result(self):
    print(f"Theta0: {self._t0}, Theta1: {self._t1}")
    with open(self.output, "w") as f:
        f.write(f"{self._t0}\n{self._t1}\n")


  def train(self):
    self.gradient_descent()
    self.unnormalize_thetas()
    self.print_result()
    if (self.b_plot_result):
      self.plot_result()
    if (self.b_plot_cost):
      self.plot_cost()

def optparse():
  parser = argparse.ArgumentParser()
  parser.add_argument('--input', '-in', action="store", dest="input", default="resources/data.csv", help="select the input file")
  parser.add_argument('--output', '-o', action="store", dest="output", default="theta.txt", help="select the output file")
  parser.add_argument('--alpha', '-a', action="store", dest="alpha", default=0.01, type=float, help="set the learing rate")
  parser.add_argument('--iteration', '-it', action="store", dest="iteration", default=10000, type=int, help="set the max number of iterations")
  parser.add_argument('--plot-result', '-pr', action="store_true", dest="plot_result", default=False, help="plot the result")
  parser.add_argument('--plot-cost', '-pc', action="store_true", dest="plot_cost", default=False, help="plot the cost evolution")

  return parser.parse_args()


def signal_handler(sig, frame):
    sys.exit(0)

if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal_handler)
  options = optparse()

  if (options.alpha > 1 or options.alpha < 0.00000001):
    options.alpha = 0.01
    
  print('Start training with this values')
  print('     Input       : ' + str(options.input))
  print('     Output      : ' + str(options.output))
  print('     Alpha       : ' + str(options.alpha))
  print('     Iterations  : ' + str(options.iteration))
  print('     Plot result : ' + str(options.plot_result))
  print('     Plot Cost   : ' + str(options.plot_cost))

  LinearRegression(options.input, options.output, options.alpha, options.iteration, options.plot_result, options.plot_cost).train()
