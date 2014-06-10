import matplotlib.pyplot as plt


def make_plots(results):
    plots = {}
    for k, v in results.items():
        fig, ax = plt.subplots()
        ax.axhline(y=v.average_params, color='black')
        y = v.resampled_params
        x = range(len(y))
        plt.fill_between(x, v.average_params-v.errs, v.average_params+v.errs,
                         alpha=0.3)
        ax.plot(y)
        ax.set_title(k)
        plots[k] = fig
    return plots