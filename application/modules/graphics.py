import matplotlib.pyplot as plt


class Graphics:
    def showGraphics(self, x, y, xName, yName, x2, y2, xName2, yName2):
        plt.figure()
        plt.subplot(2, 1, 1)
        plt.plot(x, y)
        plt.xlabel(xName)
        plt.ylabel(yName)

        plt.subplot(2, 1, 2)
        h = [32, 63, 126, 250, 510, 1000]
        plt.vlines(h, 0, y2.max(), color='g', linestyle='--')
        plt.plot(x2[0:len(x2) // 3], y2[0:len(y2) // 3])
        plt.xlabel(xName2)
        plt.ylabel(yName2)
        plt.tight_layout()