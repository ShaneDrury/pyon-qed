from pyon.lib.fitting.base import FitParams


def pad(samples, num_lec):
    """
    Build super jackknife block.
    There are 190 QCD LECs, but only 98 + 45 = 143 delta m square jk samples
    Fill the rest with the average of them i.e.:
    Q0,   Q1,   Q2,   Q3,   Q4
    A0,   A1,   Aave, Aave, Aave
    Bave, Bave, Bave, B0,   B1

    Where Q are the QCD LEC jackknife samples, and A and B are the 0.005 and
    0.01 jackknife samples.

    000-097: m0.005 is from data, m0.01 is from ave.
    098-100: both m0.005 and m0.01 are from ave.
    101-145: m0.005 is from ave, m0.01 is from data.
    146-189: both m0.005 and m0.01 are from ave.
    """
    new_dict = {}
    for k, v in samples.items():
        ml1, ml2, q1, q2, m_l = k
        if m_l == 0.005:
            new_v = v.resampled_params
            for i in range(num_lec - len(v.resampled_params)):
                new_v.append(v.average_params)
            new_dict[k] = FitParams(v.average_params, v.errs, new_v)
        elif m_l == 0.01:
            new_v = []
            for i in range(100):  # Matches Ran's Code
                new_v.append(v.average_params)
            new_v += v.resampled_params

            for i in range(num_lec - len(new_v)):
                new_v.append(v.average_params)

            new_dict[k] = FitParams(v.average_params, v.errs, new_v)
        else:
            raise ValueError("m_l not 0.005 or 0.01")
    return new_dict