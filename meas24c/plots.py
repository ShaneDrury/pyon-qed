import matplotlib.pyplot as plt


def delmsq_plots(results):
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


def mass_plots(results):
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


def correlator_plots(results):
    plots = {}
    for k, v in results.items():
        fig, ax = plt.subplots()
        y = v.central_data
        x = range(len(y))
        ax.set_yscale("log", nonposy='clip')
        ax.grid(True)
        ax.errorbar(x, y, yerr=v.central_errs)
        ax.set_xlim(0, len(y)/2)
        ax.set_title(k)
        plots[k] = fig

    for k, v in results.items():
        fig, ax = plt.subplots()
        y = v.effective_mass
        x = range(len(y))
        ax.grid(True)
        ax.errorbar(x, y, yerr=v.effective_mass_errs)
        ax.set_xlim(0, len(y)/2)
        ax.set_title(k)
        plots[str(k) + '_eff_mass'] = fig
    return plots