import matplotlib.pyplot as plt
import matplotlib
matplotlib.use('Agg')

class DrawChart:
  def bar(self, x, y, path):
    plt.bar(x, y)
    plt.savefig(f'{path}/static/images/chart.png')
    plt.close()

  def line(self, x, y, path):
    plt.plot(x, y)
    plt.savefig(f'{path}/static/images/chart.png')
    plt.close()