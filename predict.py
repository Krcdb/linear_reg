from utils import *
import plotly.graph_objects as go
import argparse
import signal
import sys


class Predict:
  def __init__(self, theta_input, data_input, plot_result):
    #data
    self.data = get_data(data_input)
    self.x = self.data[0]
    self.y = self.data[1]
    
    self.T = get_thetas(theta_input)
    self.b_plot_result = plot_result


  def plot_result(self, km, price):
    fig = go.Figure()

    fig.add_trace(go.Scatter(x=self.x, y=self.y, mode='markers', name='Data'))
    
    x_min_data = min(self.x)
    x_max_data = max(self.x)
    x_range = x_max_data - x_min_data
    x_start = x_min_data - 0.2 * x_range
    x_end = x_max_data + 0.2 * x_range

    y_start = self.T[0] + self.T[1] * x_start
    y_end = self.T[0] + self.T[1] * x_end

    fig.add_trace(go.Scatter(
        x=[x_start, x_end],
        y=[y_start, y_end],
        mode='lines',
        name='Regression Line'
    ))
    fig.add_trace(go.Scatter(
          x=[km],
          y=[price],
          mode='markers',
          marker=dict(color='red', size=10, symbol='x'),
          name='Predicted Point'
      ))

    fig.update_layout(title='Price vs. Kilometers',
                      xaxis_title='Kilometers',
                      yaxis_title='Price')
    fig.show()
  
  def prompt(self):
    while True:
      user_input = input("Enter a value in kilometers (or type 'exit' to quit): ").strip()
      if user_input.lower() == "exit":
        print("Exiting.")
        break
      try:
        km = float(user_input)
        self.predict(km)
      except ValueError:
        print("Invalid input. Please enter a numeric value or 'exit'.")

  def predict(self, km):
    predicted_price = int(self.T[0] + self.T[1] * km)
    print(f"The predicted price is {int(predicted_price)}")
    if (self.b_plot_result):
      self.plot_result(km, predicted_price)
    
    
def optparse():
  parser = argparse.ArgumentParser()
  parser.add_argument('--theta_input', '-ti', action="store", dest="theta_input", default="theta.txt", help="select the theta input file")
  parser.add_argument('--data_input', '-di', action="store", dest="data_input", default="resources/data.csv", help="select the theta input file")
  parser.add_argument('--plot-result', '-pr', action="store_true", dest="plot_result", default=False, help="plot the result")

  return parser.parse_args()

def signal_handler(sig, frame):
    sys.exit(0)
    
if __name__ == '__main__':
  signal.signal(signal.SIGINT, signal_handler)
  options = optparse()
    
  print('Start predicting with this values')
  print('     Theta Input : ' + str(options.theta_input))
  print('     Data Input  : ' + str(options.data_input))
  print('     Plot result : ' + str(options.plot_result))
  
  Predict(options.theta_input, options.data_input, options.plot_result).prompt()
