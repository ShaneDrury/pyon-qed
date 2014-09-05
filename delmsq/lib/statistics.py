def equivalent_params(m1, m2, q1, q2):
    """
    Given two charges, return a list of the charges of the quarks that give
    the same meson mass. Used to average over equivalent correlators for
    improved statistics. Also return the original set of parameters.
    Can swap the sign of the charges and keep the masses the same, swap the
    masses AND the charges, or swap the masses and keep the charges the same.
    """
    return [[m1, m2, q1, q2], [m1, m2, -q1, -q2], [m2, m1, q2, q1],
            [m2, m1, -q2, -q1]]


# def equivalent_params_m_l(m1, m2, q1, q2, m_l):
#     return [(m1, m2, q1, q2, m_l),
#             (m1, m2, -q1, -q2, m_l),
#             (m2, m1, q2, q1, m_l),
#             (m2, m1, -q2, -q1, m_l)]
#
#
# class SymmetricDict(dict):
#     def __getitem__(self, key):
#         for k in equivalent_params_m_l(*key):
#             print(k)
#             try:
#                 r = super().__getitem__(k)
#                 return r
#             except KeyError:
#                 pass
#         raise KeyError(key)