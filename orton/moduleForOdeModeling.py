"""
28 September 2015

Adapted from Sergion Rossell
Module for simulating kinetic models based on ODEs.
"""

################################################################################
# FUNCTIONS


def subsIdsByValue(rateEq, transDict):
    """
    Takes a rate equation (rateEq), which is a string, and substitutes the
    keys in transDict for their values. 
    ACCEPTS
    rateEq [str] rate equation
    transDict [dict] {key : value}

    RETURNS
    s [str] rateEq with keys substituted by values
    """
    import re
    s = rateEq[:]
    for key in transDict:
        if type(transDict[key]) != str:
            s = re.sub(r'\b%s\b' % key, str(transDict[key]), s)
        else:
            s = re.sub(r'\b%s\b' % key, transDict[key], s)
    return s


def createRateFuncFromEq(rateEq, transDict):
    """
    Takes a rate equation as a string (rateEq) and substitutes parameter
    and species names by their values or vector variables in transDict
    and creates a lambda function that dependens on the vector variables.

    Uses the function subsIdsByValue to substitute the keys in transDict
    for their values.

    ACCEPTS
    rateEq [str] rate equation
    transDict [dict] {paramId : paramValue, speciesId : x[..]}

    RETURNS [lambda] function that depends on the vector x
    """
    return lambda x: eval(subsIdsByValue(rateEq, transDict))


def createRateVector(idSp, idRs, rateEqDict, paramDict):
    """
    Creates a rate vector v = f(x) where x is the concentration vector
    of species. The vector conserves the order in idRs

    Uses the function createRateFuncFromEq to produce a lambda function
    for each rate equation if rateEqDict

    ACCEPTS
    idSp [list] ordered species ids
    idRs [list] ordered reaction ids
    rateEqDict [dict] {rxnId : rate equation (as a string)
    paramDict [dict] {paramId : paramValue}

    RETURNS [list of lambda functions] v = f(x)
    """
    # species names to concentration vector 'x'
    idSp_dict = dict(zip(idSp, ['x[%i]' % i for i, sp in enumerate(idSp)]))
    subsDict = paramDict.copy()
    subsDict.update(idSp_dict)
    return lambda x: [i(x) for i in [
        createRateFuncFromEq(rateEqDict[r], subsDict) for r in idRs]]


def derivRateEqRespectToSp(rateEq, sp, transDict):
    """
    Calculates the derivative of a rate equation  with respect to 
    the concentration of a species

    ACCEPTS
    rateEq [str] rate equation
    sp [str] id of the species with respect to which take the derivative
    transDict [dict] {paramId : paramValue, speciesId : concentration (float)}

    RETURNS [float] derivative of rateEq with respect to sp at the state defined
        in transDict
    """
    from scipy.misc import derivative
    d = transDict.copy()
    spVal = d.pop(sp)
    d[sp] = 'y'

    def f(y): return eval(subsIdsByValue(rateEq, d))
    # stepsize for derivative (from Pysces source code, which acknowledges Sauro)
    h = spVal > 1E-12 and spVal*1E-1 or 1E-12
    return derivative(f, spVal, h)


def unscalledElasticities(idSp, idRs, rateEqDict, transDict):
    """
    Calculates the unscalled elasticity matrix

    ACCEPTS
    idSp [list] ordered species ids
    idRs [list] ordered reaction ids
    rateEqDict [dict] {rxnId : rate equation (as a string)
    transDict [dict] {paramId : paramValue, speciesId : concentration (float)}

    RETURNS [2d array] unscalled elasticity matrix
    """
    from numpy import array
    uelas = []
    for rxn in idRs:
        l = []
        for sp in idSp:
            l.append(derivRateEqRespectToSp(rateEqDict[rxn], sp, transDict))
        uelas.append(l)
    return array(uelas)


def jacobian(idSp, idRs, rateEqDict, S, transDict):
    """
    Calculates the jacobi matrix

    ACCEPTS
    idSp [list] ordered species ids
    idRs [list] ordered reaction ids
    rateEqDict [dict] {rxnId : rate equation (as a string)
    transDict [dict] {paramId : paramValue, speciesId : concentration (float)}

    RETURNS [2d array] jacobi matrix
    """
    from numpy import dot
    uelas = unscalledElasticities(idSp, idRs, rateEqDict, transDict)
    return dot(S, uelas)


################################################################################
# TESTING
if __name__ == '__main__':
    from numpy import array, dot, arange
    from scipy.integrate import odeint
    from scipy.optimize import fsolve
    ########################################
    # INPUTS
    idRs = [
        'Raf1ByRasAct',
        'Raf1byPPtaseDeact',
        'MekbyRaf1Act',
        'MekDeact',
        'ErkAct',
        'ErkDeact',
    ]

    rates = {
        'Raf1ByRasAct': ' kRasToRaf1 * RasActive * (Raf1total - Raf1Active) / ((Raf1total - Raf1Active) + KmRasToRaf1)',
        'Raf1byPPtaseDeact': 'kdRaf1 * Raf1PPtase * Raf1Active / (Raf1Active + KmdRaf1)',
        'MekbyRaf1Act': 'kpRaf1 * Raf1Active * (MekTotal - MekActive) / ((MekTotal - MekActive) + KmpRaf1)',
        'MekDeact': 'kdMek * PP2AActive * MekActive / (MekActive + KmdMek)',
        'ErkAct': 'kpMekCytoplasmic * MekActive * (ErkTotal - ErkActive) / ((ErkTotal - ErkActive) + KmpMekCytoplasmic)',
        'ErkDeact': 'kdErk * PP2AActive * ErkActive / (ErkActive + KmdErk)',
    }

    idSp = [
        'Raf1Active',
        'MekActive',
        'ErkActive'
    ]

    init = [
        0.,  # Raf1Active
        0.,  # MekActive
        0.,  # ErkActive
    ]

    S = [
        [1, -1, 0, 0, 0, 0],
        [0, 0, 1, -1, 0, 0],
        [0, 0, 0, 0, 1, -1]
    ]

    timeRange = arange(0, 150, 0.01)

    param = {
        #{{{
        'RasActive': 4000.5,
        'Raf1total': 120000.0,
        'Raf1PPtase': 120000.0,
        #
        'MekTotal': 600000.0,
        'PP2AActive': 120000.0,
        #
        'ErkTotal':  600000.0,
        # end
        'KmAkt': 653951.0,
        'KmC3G': 10965.6,
        'KmC3GNGF': 12876.2,
        'KmEGF': 6086070.0,
        'KmNGF': 2112.66,
        'KmPI3K': 184912.0,
        'KmPI3KRas': 272056.0,
        'KmRaf1ByAkt': 119355.0,
        'KmRap1ToBRaf': 1025460.0,
        'KmRapGap': 295990.0,
        'KmRasGap': 1432410.0,
        'KmRasToRaf1': 62464.6,
        'KmSos': 35954.3,
        'KmdBRaf': 10879500.0,
        'KmdErk': 3496490.0,
        'KmdMek': 518753.0,
        'KmdRaf1': 1061.71,
        'KmdSos': 896896.0,
        'KmpBRaf': 157948.0,
        'KmpMekCytoplasmic': 1007340.0,
        'KmpP90Rsk': 763523.0,
        'KmpRaf1': 4768350.0,
        'cell': 1.0,
        'kAkt': 0.0566279,
        'kC3G': 1.40145,
        'kC3GNGF': 146.912,
        'kEGF': 694.731,
        'kNGF': 389.428,
        'kPI3K': 10.6737,
        'kPI3KRas': 0.0771067,
        'kRap1ToBRaf': 2.20995,
        'kRapGap': 27.265,
        'kRasGap': 1509.36,
        'kRasToRaf1': 0.884096,
        'kSos': 32.344,
        'kdBRaf': 441.287,
        'kdErk': 8.8912,
        'kdMek': 2.83243,
        'kdRaf1': 0.126329,
        'kdRaf1ByAkt': 15.1212,
        'kdSos': 1611.97,
        'kpBRaf': 125.089,
        'kpMekCytoplasmic': 9.85367,
        'kpP90Rsk': 0.0213697,
        'kpRaf1': 185.759,
        'krbEGF': 2.18503e-05,
        'krbNGF': 1.38209e-07,
        'kruEGF': 0.0121008,
        'kruNGF': 0.00723811
        #}}}
    }

    ########################################
    # STATEMENTS

    ####################
    # ODE simulation

    # rate vector
    v = createRateVector(idSp, idRs, rates, param)

    # ODES
    def odes(x, t):
        return dot(S, v(x))

    # integrating the odes
    xt = odeint(odes, init, timeRange)

    ####################
    # STEADY-STATE solution
    xss = fsolve(odes, xt[-1], None)

    ####################
    # Computing the Jacobi matrix
    ssDict = dict(zip(idSp, xss))
    diffSubs = param.copy()
    diffSubs.update(ssDict)

    jac = jacobian(idSp, idRs, rates, S, diffSubs)
