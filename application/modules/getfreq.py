import base64
from io import BytesIO
import math
from scipy import fft, arange, fftpack
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
import json
import os
from application.modules.graphics import Graphics


class GetFrequency:

    dict_max_freq = dict()

    def readWave(self, song):
        return wavfile.read(song)

    def getfreq(self, song, start=None, end=None):
        sample_rate, signal = self.readWave(song)
        print("Frequency sampling", sample_rate)
        channels = len(signal.shape)
        print("Channels", channels)

        if channels == 2:
            y0 = signal.sum(axis=1) / 2
        else:
            y0 = signal
        print('y0', len(y0), y0)
        print(start, end)
        t0 = np.arange(len(y0)) / float(sample_rate)  # временнной массив

        if start is not None and end is not None:
            # end += 1
            y = y0[int(start*sample_rate): int(end*sample_rate)]
            t = t0[int(start * sample_rate): int(end * sample_rate)]
            print('cut y', len(y), y)
        else:
            start, end = 0, max(t0)
            y = y0
            t = t0

        print('t', len(t), max(t), t)
        print("start", start * sample_rate, end * sample_rate)
        frq, X = self.frequency_spectrum(y, sample_rate)

        # print(len(frq), len(X))
        # print(len(t[int(start * sample_rate): int(end * sample_rate)]), len(
        #                       y[int(start * sample_rate): int(end * sample_rate)]))
        self.showGraphics(t, y, 't', 'Amplitude', frq, X, 'Freq (Hz)', '|X(freq)|')

        print('frq', len(frq), frq)
        print('X', len(X), X)
        freqs = fftpack.fftfreq(len(y))
        freqs = freqs[range(len(freqs) // 2)]
        print('freqs', len(freqs), freqs)

        # Graphics.showGraphics(t, y, 't', 'Amplitude', frq, X, 'Freq (Hz)', '|X(freq)|')

        ###################################

        print('____________________________________________________')
        count = 2
        time_in_sec = np.linspace(start*sample_rate, end * sample_rate, math.ceil(end-start)*count+1)  # временной массив соответсвует каждой секунде
        print('tsec', len(time_in_sec), time_in_sec)

        maxF = np.array([])  # zeros(len(time_in_sec))
        tsec = np.array([])
        n = len(time_in_sec)
        domF = [[] for j in range(n)]
        self.dict_max_freq = dict()
        for j in range(n - 1):
            y1 = y0[int(time_in_sec[j]): int(time_in_sec[j + 1])]
            print('y1', time_in_sec[j])

            frq, X = self.frequency_spectrum(y1, sample_rate)

            self.showGraphics(t0[int(time_in_sec[j]):int(time_in_sec[j + 1])], y1, 't', 'Amplitude', frq, X, 'Freq (Hz)',
                         '|X(freq)|')

            maxA = np.zeros(len(frq))
            maxANH = [0 for j in range(7)]

            # showGraphics(t[int(time_in_sec[j]):int(time_in_sec[j+1])], y1, 't', 'Amplitude',    frq, X, 'Freq (Hz)', '|X(freq)|')

            for i in range(len(X) - 1):
                if (X[i - 1] < X[i] and X[i] > X[i + 1] and 0 < X[i] and frq[i] < 1040):
                    number_of_harmonic = self.harmonic(frq[i])

                    if (X[i] > maxANH[number_of_harmonic] and X[i] > max(maxA)):
                        # print(number_of_harmonic)
                        # print(frq[i])
                        maxA[i] = X[i]

                        if (maxANH[number_of_harmonic] == 0):
                            maxF = np.append(maxF, frq[i])
                            tsec = np.append(tsec, time_in_sec[j])
                            maxANH[number_of_harmonic] = X[i]
                            domF[j].append(round(frq[i], 3))

                        else:
                            domF[j][len(domF[j])-1] = round(frq[i], 3)
                            maxF[len(maxF) - 1] = frq[i]
                            tsec[len(tsec) - 1] = time_in_sec[j]

            print('For ', j, ' part ', ' freq ', domF[j])
            start_time = round(time_in_sec[j] / sample_rate, 3)
            end_time = round(time_in_sec[j + 1] / sample_rate, 3)
            self.dict_max_freq[str(start_time) + ' - ' + str(end_time)] = domF[j]

        print("len(time_in_sec) ", time_in_sec)
        print("time_in_sec//sr", time_in_sec // sample_rate)
        plt.figure()
        h = [32, 63, 126, 250, 510, 1000]
        plt.hlines(h, start, end, color='r', linestyle='--')
        plt.scatter((tsec / sample_rate ), maxF)
        plt.xlabel('time_in_sec')
        plt.ylabel('maxF')
        plt.tight_layout()

        figfile = BytesIO()
        plt.savefig(figfile, format='png')
        figfile.seek(0)
        figdata_png = base64.b64encode(bytearray(figfile.getvalue()))
        plt.show()
        return figdata_png.decode('utf-8')

    def harmonic(self, val):
        harmonic = {'1': [32.7, 61.75], '2': [65.41, 123.48], '3': [130.82, 247],'4': [261, 495],'5':[520, 990],'6': [1040, 2000], '7': [2010, 4000]}

        if 32 <= val < 63:
            return 1
        if val < 32:
            return 0
        elif 63 <= val < 125:
            return 2
        elif 125 <= val < 250:
            return 3
        elif 250 <= val < 510:
            return 4
        elif 510 <= val < 990:
            return 5
        elif 990 <= val < 2000:
            return 6

    def frequency_spectrum(self, x, sf):
        x = x - np.average(x)  #
        n = len(x)

        k = arange(n)   # массив с индексами от 0 до n(не включительно)
        tarr = n / float(sf)
        frqarr = k / float(tarr)  #

        frqarr = frqarr[:(n // 2)-1]  #

        x = fft(x) / n  # fft и нормализация
        x = x[:(n // 2)-1]
        # print(x)
        for elem in x:
            elem = math.sqrt(elem.real*elem.real + elem.imag*elem.imag)
        return frqarr, abs(x)

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
        plt.show()
