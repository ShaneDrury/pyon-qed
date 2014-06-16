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


def mass_plots_unchg(results):
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


def equiv_q(q1, q2):
    return [(-q1, -q2), (q2, q1), (-q2, -q1)]


def mass_plots_chg(results):
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

    # lm = [0.005, 0.01, 0.02, 0.03]  # light masses
    # m_res = 3.131e-3
    #
    # def r(*args):
    #     return results[args].average_params
    #
    # y_udbar = [r(0.005, 0.005, -2, -1), r(0.01, 0.01, -2, -1),
    #            r(0.02, 0.02, 2, 1), r(0.03, 0.03, -2, -1)]
    #
    # # y_uubar = [results[(ml, ml, q_uubar[0], q_uubar[1])] for ml in lm]
    # # y_ddbar = [results[(ml, ml, q_ddbar[0], q_ddbar[1])] for ml in lm]
    # x = np.array(lm) + m_res
    # fig, ax = plt.subplots()
    # ax.plot(x, y_udbar)
    # # ax.plot(x, y_uubar)
    # # ax.plot(x, y_ddbar)
    # ax.set_title('Meson mass-squared splittings 24^3')
    #
    # plots['delmsq_vs_ml'] = fig

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