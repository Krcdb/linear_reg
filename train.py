import plotly.graph_objects as go
from utils import *
import argparse


class linear_regression:
    def __init__(self, input, alpha, iteration):
        

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


    def gradient_descent(self):

        for _ in range(self.max_iteration):
            derivative_cost0 = 0
            derivative_cost1 = 0

            for i in range(self.m):
                error = (self.t0 + self.t1 * self.x[i]) - self.y[i]
                derivative_cost0 += error
                derivative_cost1 += error * self.x[i]

            self.t0 = self.t0 - self.alpha * (2 / self.m) * derivative_cost0
            self.t1 = self.t1 - self.alpha * (2 / self.m) * derivative_cost1

            self.iteration += 1
    
    def unnormalize_thetas(self):
        x_min, x_max = min(self._x), max(self._x)
        y_min, y_max = min(self._y), max(self._y)

        scale_x = x_max - x_min
        scale_y = y_max - y_min

        self._t1 = self.t1 * scale_y / scale_x
        self._t0 = self.t0 * scale_y - self._t1 * x_min + y_min

    def plot_result(self):
        fig = go.Figure()

        fig.add_trace(go.Scatter(x=self._x, y=self._y, mode='markers', name='Data'))

        y_pred = [self._t0 + self._t1 * xi for xi in self._x]
        fig.add_trace(go.Scatter(x=self._x, y=y_pred, mode='lines', name='Regression Line'))

        fig.update_layout(title='Price vs. Kilometers',
                          xaxis_title='Kilometers',
                          yaxis_title='Price')
        fig.show()

    def print_result(self):
        print(f"Theta0: {self._t0}, Theta1: {self._t1}")

    def train(self):
        self.gradient_descent()
        self.unnormalize_thetas()
        self.print_result()
        self.plot_result()




def optparse():
    parser = argparse.ArgumentParser()
    parser.add_argument('--input', '-in', action="store", dest="input", default="resources/data.csv")
    parser.add_argument('--alpha', '-a', action="store", dest="alpha", default=0.01, type=float)
    parser.add_argument('--iteration', '-it', action="store", dest="iteration", default=100000, type=int)

    return parser.parse_args()


if __name__ == '__main__':
    
    options = optparse()

    if (options.alpha > 1 or options.alpha < 0.00000001):
        options.alpha = 0.01
    
    print('Start training with this values')
    print('     Alpha       : ' + str(options.alpha))
    print('     Iterations  : ' + str(options.iteration))

    linear_regression(options.input, options.alpha, options.iteration).train()
