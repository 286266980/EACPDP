import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

def processDatas(datas):
    baseline_data = 'CBSplus'
    data_filter = ['BF', 'PF', 'KF', 'DFAC','TCA', 'BDA', 'JDA', 'JPDA','TNB']
    metric_datas = []
    functions = []
    for function in data_filter:
        metric_datas.append(datas[function] - datas[baseline_data])
        functions.append(function)
    return metric_datas, functions

def load_color(dataset, metric, functions):
    colors_path = './classify/Testdata/%s/%s.csv' % (dataset, metric)
    datas = pd.read_csv(colors_path)
    colors = []
    for function in functions:
        if datas[function][0] < 0.05:
            colors.append('red')
        else:
            colors.append('black')
    return colors

def drawFigure(metric_datas, functions, metric, dataset):
    ymax = 0
    ymin = 100
    for data in metric_datas:
        if ymax < max(data):
            ymax = max(data)
        if ymin > min(data):
            ymin = min(data)

    plt.rc('font', family='Times New Roman')
    fig, ax = plt.subplots(figsize=(4, 3))
    ax.tick_params(direction='in')

    xticks = np.arange(1, len(functions) * 1.5, 1.5)
    figure = ax.boxplot(metric_datas,
                        notch=False,  # notch shape
                        sym='r+',  # blue squares for outliers
                        vert=True,  # vertical box aligmnent
                        meanline=True,
                        showmeans=False,
                        patch_artist=False,
                        showfliers=False,
                        positions=xticks,
                        boxprops={'color': 'red'}
                        )
    colors = load_color(dataset, metric, functions)
    for i in range(len(colors)):
        k = figure['boxes'][i]
        k.set(color=colors[i])
        k = figure['medians'][i]
        k.set(color=colors[i], linewidth=2)
        k = figure['whiskers'][2 * i:2 * i + 2]
        for w in k:
            w.set(color=colors[i], linestyle='--')
        k = figure['caps'][2 * i:2 * i + 2]
        for w in k:
            w.set(color=colors[i])

    plt.xlim((0, 14))
    plt.xticks(xticks, functions, rotation=45, weight='heavy', fontsize=12, ha='center')
    plt.yticks(fontsize=12,weight='heavy')
    plt.ylabel(metric, fontsize=12,weight='heavy')
    plt.rcParams['xtick.direction'] = 'in'
    plt.rcParams['ytick.direction'] = 'in'
    plt.axhline(y=0, color='blue')
    plt.axvline(6.3, color='grey', linestyle=':')
    plt.title(
        "     Data filter    "
        "    Transfer learning"
        , fontsize=14, loc='left',weight='heavy')
    Path('../classify/figures/{0}'.format(dataset)).mkdir(parents=True, exist_ok=True)
    output_path = '../classify/figures/%s/%s.jpg' % (dataset, metric)
    foo_fig = plt.gcf()
    foo_fig.savefig(output_path, format='jpg', dpi=1000, bbox_inches='tight')

    plt.clf()
    plt.close()

def read_data(dataset_path, metric):
    functions = ['CBSplus', 'BF', 'PF', 'KF', 'DFAC', 'TCA', 'BDA', 'JDA', 'JPDA','TNB']
    datas = {}
    for function in functions:
        data_path = '{0}/{1}.csv'.format(dataset_path,function)
        raw_datas = pd.read_csv(data_path)
        raw_datas = raw_datas[metric].values
        datas[function] = raw_datas
    return datas

def BoxPlot(results_path):
    metrics = ['Precision', 'Recall', 'F1']
    for dataset in os.listdir(results_path):
        for metric in metrics:
            dataset_path = results_path + '%s' % dataset
            datas = read_data(dataset_path, metric)
            metric_datas, functions = processDatas(datas)  # metric_datas：our functions - CBS+
            drawFigure(metric_datas, functions, metric, dataset)
            print('Drawing %s_%s .....' % (dataset, metric))

if __name__ == '__main__':
    BoxPlot(r'../../output_classify/')

