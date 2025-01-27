import matplotlib.pyplot as plt
import numpy as np


logFiles = ["/Users/chuck/AIE13/Explore/lession_detect/log/log.traintest_05-17_21-18-01.3DCE1image3slice"]
legend = ["Train"]
keywords = ['Epoch', 'Batch', 'RPNLogLoss=', 'RPNL1Loss=', 'RCNNLogLoss=', 'RCNNL1Loss=']


def draw_loss(logFiles, legend, keywords, smooth=0, ylim=None):
    legends = []
    for iFile in range(len(logFiles)):
        vals = {key1: [] for key1 in keywords}
        accs = []
        with open(logFiles[iFile]) as f:
            lines = f.readlines()

        for line in lines:
            if line.startswith('INFO:root:Epoch '):
                line = line.replace(',', ' ')
                for key1 in keywords:
                    s = line.split(key1)
                    if len(s) == 1: continue

                    assert len(s) == 2, 'multiple terms found'
                    vals[key1].append(float(s[1].split()[0]))
            elif line.startswith('recall@.5='):
                accs.append(float(line.split('recall@.5=')[1]))

        epochs = np.array(vals['Epoch'])
        iters = np.array(vals['Batch'])
        del vals['Epoch']
        del vals['Batch']
        epochs_dec = epochs + iters/iters.max()

        for key1 in vals.keys():
            loss = np.array(vals[key1])
            if smooth > 0:
                loss = np.convolve(loss, np.ones(smooth, dtype=float)/smooth, mode='valid')
            plt.plot(epochs_dec[:loss.shape[0]], loss)
            legends.append(legend[iFile]+' '+key1)

        print(accs)

    plt.xlabel('Epoch')
    plt.ylabel('loss')
    if ylim is not None: plt.ylim(ylim)

    plt.legend(legends)
    plt.show()


if __name__ == '__main__':
    draw_loss(logFiles, legend=legend, keywords=keywords, smooth=10)
