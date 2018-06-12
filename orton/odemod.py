"""Build and simulate Orton ODE model."""

# 28 August 2014

# classes to build the Orton ODE model and simulate
# parameter perturbations to the model.

# """
import copy
import sympy
import numpy as np
import pylab as p
# from numpy import arange, dot
import scipy
from scipy.integrate import odeint
from scipy.optimize import fsolve

###############################################################################
#
# CLASSSES
#
###############################################################################


###############################################################################
# ODE model class

class OdeModelOrton(object):
    """ODE model."""

    def __init__(self, mDict):
        """
        mDict: Dictionary object containing model description.

        (including decomposition in modules)

        HOW TO INTEGRATE ODES:

        m = OdeModel(S, idSp, idRs, rateDict, param, init)#simTime
        m.performSubstitutions()
        m.buildRateVector()

        from scipy.integrate import odeint

        def odes(x, t):
            return dot(m.S, m.v(x, m.rateVector))

        xt = odeint(odes, m.init, simTime)
        """
        self.spDict = copy.deepcopy(mDict['spDict'])
        self.S = copy.deepcopy(mDict['S'])
        self.idSp = copy.deepcopy(mDict['idSp'])
        self.idRs = copy.deepcopy(mDict['idRs'])
        self.rateDict = copy.deepcopy(mDict['rateLaws'])
        self.param = copy.deepcopy(mDict['param'])
        self.nodes = copy.deepcopy(mDict['nodes'])
        self.modules = copy.deepcopy(mDict['modules'])
        self.init = self._buildInit(mDict)
        self.interactions = self._gen_interactions()
        self.imap = self._gen_imap()  # Interaction map
        self.rloc_symbols = self._gen_rloc_symbols()  # Local response matrix
        self._updateModel()

    def setParam(self, par, val):
        """Set parameters par to value val.

        Inputs:
        par:    Parameter name or list of parameter names
        newval: New parameter value or list of new parameter values
        """
        if type(par) is list and type(val) is list:
            for i in range(len(par)):
                p = par[i]
                v = val[i]
                self.param[p] = v
                if p not in self.param.keys():
                    print("WARNING: model does not contain parameter " + p)
        else:
            if par not in self.param.keys():
                print("WARNING: model does not contain parameter " + par)
            self.param[par] = val
        self._updateModel()

    def setInit(self, sp, newval):
        """Set initial concentration of species.

        Inputs:
        sp: Species names
        newval: new initial value
        """
        if type(sp) is list:
            assert len(sp) == len(newval)
            for i in range(len(sp)):
                self.spDict[sp[i]]['initConcentration'] = newval[i]
        else:
            self.spDict[sp]['initConcentration'] = newval
        self._updateModel()

    def get_species_names(self, species=None):
        """Return name of species."""
        if not species:
            species = self.idSp
        if type(species) is list:
            return [self.spDict[sp]['name'] for sp in species]
        elif type(species) is str:
            return self.spDict[species]['name']
        else:
            print("WARNING: " + str(species) + "should be sring or list of" +
                  " srings")

    def getRateVertor(self):
        """Build and return rateVector."""
        return self._createRateVector()

    def _updateModel(self):
        """Update model after changes to e.g. parameters are made."""
        self._updateInit()
        # self._substituteParameterValues()
        # self._substituteVectorOfVariables()
        self.rateVector = self._createRateVector()

    def _buildInit(self, mDict):
        init = []  # you may choose to change initial conditions
        for sp in mDict['idSp']:
            init.append(mDict['spDict'][sp]['initConcentration'])
        return init

    def _updateInit(self):
        init = []  # you may choose to change initial conditions
        for sp in self.idSp:
            init.append(self.spDict[sp]['initConcentration'])
        self.init = init
        return

    def _gen_rloc_symbols(self):
        nn = len(self.nodes)
        mat = np.zeros((nn, nn), dtype=sympy.Symbol)
        for i in range(nn):
            for j in range(nn):
                if i == j:
                    mat[i][j] = sympy.Symbol('r_i_i')
                else:
                    mat[i][j] = sympy.Symbol('r_' + self.nodes[i] + '_' +
                                             self.nodes[j])
        return(mat)

    def _gen_interactions(self):
        inacts = set()
        for key, mod in self.modules.items():
            inputs = set.intersection(set(self.nodes), mod['input_from'])
            # Assume only one output
            output = set.intersection(set(self.nodes), mod['species'])
            for i in inputs:
                for o in output:
                    inacts.add((o, i))
        return inacts

    def _gen_imap(self):
        """Generate square matrix containing interacts between nodes.

        i_ij = 1: i affects j
        i_ij = 0: i does not affect j
        """
        nn = len(self.nodes)
        im = np.zeros((nn, nn), dtype=int)
        for i in self.interactions:
            indexi = self.nodes.index(i[0])
            indexj = self.nodes.index(i[1])
            im[indexi][indexj] = 1
        return im

    def _subsIdsByValue(self, rateEq, transDict):
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

    def _createRateFuncFromEq(self, rateEq, transDict):
        """ Takes a rate equation as a string (rateEq) and substitutes parameter
        and species names by their values or vector variables in transDict
        and creates a lambda function that dependens on the vector variables.

        Uses the function subsIdsByValue to substitute the keys in transDict
        for their values.

        ACCEPTS
        rateEq [str] rate equation
        transDict [dict] {paramId : paramValue, speciesId : x[..]}

        RETURNS [lambda] function that depends on the vector x
        """
        return lambda x: eval(self._subsIdsByValue(rateEq, transDict))

    def _createRateVector(self):
        """ Creates a rate vector v = f(x) where x is the concentration vector
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
        idSp_dict = dict(zip(self.idSp, ['x[%i]' % i for i, sp in
                                         enumerate(self.idSp)]))
        subsDict = self.param.copy()
        subsDict.update(idSp_dict)
        return lambda x: [i(x) for i in [
            self._createRateFuncFromEq(self.rateDict[r], subsDict) for r in
            self.idRs]]

    # def _parametrizeRateLaw(self, rateLaw, pList):
    #     """
    #     Takes one rate law (rateLaw) as a string and substitutes the parameter
    #     ids (keys in parameters) for their values (values in parameter).
    #     ACCEPTS:
    #     rateLaw [str] rate law
    #     parameters [dict] {id : value} Dictionary of parameters
    #     pList [list] list of parameter ids in descending length order (to
    #         avoid mismathches between overlaping ids (e.g. mapk and mapkkk)
    #     """
    #     s = copy.copy(rateLaw)
    #     for key in pList:
    #         s = s.replace(key, '%' + '(%s)s' % key)
    #         s = s % self.param
    #     return s

    # def _substituteParameterValues(self):
    #     # 1. Ordering parameter ids by lenght to avoid
    #     # mismatching (e.g. mapk and mapkkk)
    #     pList = orderStringsByLength(self.param.keys())
    #     self.rateDictParam = {}
    #     for key in self.rateDict:
    #         self.rateDictParam[key] = self._parametrizeRateLaw(
    #             self.rateDict[key], pList)

    # def _substituteVectorOfVariables(self):
    #     # from utils import orderStringsByLength
    #     idDict = {}
    #     for i, sp in enumerate(self.idSp):
    #         idDict[sp] = 'x[%i]' % i
    #
    #     idList = orderStringsByLength(idDict.keys())
    #     self.rateDictVars = {}
    #     for rxn in self.rateDictParam:
    #         s = self.rateDictParam[rxn]
    #         for sp in idList:
    #             s = s.replace(sp, '%' + '(%s)s' % sp)
    #             s = s % idDict
    #         self.rateDictVars[rxn] = s  # % idDict
    #
    # def _buildRateVector(self):
    #     self.rateVector = [self.rateDictVars[rxn] for rxn in self.idRs]

    # def odes(self):
    #     s = 'lambda x, eq'
    #     v = eval(s + ': [eval(i) for i in eq]')
    #     return dot(self.S, v(x, self.rateVector))


#############################################################################
# SimPerturbation class


class SimPerturbations(OdeModelOrton):
    """
    Goal:   Generate and store simulations of model perturbations. These can
            later be used to formulate linear/convex programming problem
    Usage:  Intialise with a OdeModelOrton object. Append perturbations using
            addPerturbation(par, newval), where par is the parameter to perturb
            and newval i the new value
    """

    def __init__(self, mD):
        OdeModelOrton.__init__(self, mD)  # self.model = model
        self.refSS = ssSol(self)
        self.rglob = np.empty([len(self.nodes), 0], dtype=float)
        self.rpert_symbols = np.empty([len(self.nodes), 0], dtype=sympy.Symbol)
        self.perturbations = []
        """
        Add a perturbation to the SimPerturbations object.

        It adds a column to rglob and to rpert_symbols, containing the response
        to the perturbation and the perturbed notes, respectively.

        Inputs:
        par:    Parameter name or list of parameter names
        newval: New parameter value or list of new parameter values
        Optional
        endTime (default = 500):  Time integration stops
        timeStep(default = 0.1): Size of iteration step
        showplot(default = False): Set True to show time simulations
        """

    def addKnockdown(self, sp, factor, endTime=1e4, timeStep=1, showplot=False):
        """
        Add a perturbation to the SimPerturbations object.

        It adds a column to rglob and to rpert_symbols, containing the response
        to the perturbation and the perturbed notes, respectively.

        Inputs:
        sp:     Name of the species to be knocked down.
        factor: float, fraction by which sp concentration is reduced.
        Optional
        endTime (default = 500):  Time integration stops
        timeStep(default = 0.01): Size of iteration step
        showplot(default = False): Set True to show time simulations
        """
        kdsol = kdSol(self, sp, factor, endTime, timeStep, showplot)
        x0 = np.array(self.getNodesConcentrations(self.refSS))
        x1 = np.array(self.getNodesConcentrations(kdsol))
        new_response = np.array(2 * (x1 - x0) / (x1 + x0)
                                ).reshape(len(self.nodes), 1)
        self.rglob = np.append(self.rglob, new_response, axis=1)

        # Update the perturbation matrix
        # Set of all species in the module affected by the perturbation
        # spc = set()
        # if type(par) is list:
        #     parset = set(par)
        # else:
        #     parset = set([par])
        # Iterate over modules to see which one are affected by knockdown
        spc = set([sp])
        for modkey, mod in self.modules.items():
            # Check if species in module
            if sp in mod['species']:
                spc.update(mod['species'])
        # Only use species that are nodes
        spc = set.intersection(spc, set(self.nodes))
        # Build the perturbation vector
        new_pert = np.zeros([len(self.nodes), 1], dtype=sympy.Symbol)
        for s in spc:
            indx = self.nodes.index(s)
            new_pert[indx] = sympy.Symbol('rp_' + s)
            # Also keep list of perturbed species
        self.perturbations.append(list(spc))
        # Add to perturbation matrix
        self.rpert_symbols = np.append(self.rpert_symbols, new_pert, axis=1)

    def addPerturbation(self, par, newval, endTime=1e4, timeStep=1,
                        showplot=False):
        """
        Add a perturbation to the SimPerturbations object.

        It adds a column to rglob and to rpert_symbols, containing the response
        to the perturbation and the perturbed notes, respectively.

        Inputs:
        par:    Parameter name or list of parameter names
        newval: New parameter value or list of new parameter values
        Optional
        endTime (default = 500):  Time integration stops
        timeStep(default = 0.1): Size of iteration step
        showplot(default = False): Set True to show time simulations
        """
        # Update the global response matrix rglob
        psol = pertSol(self, par, newval, endTime, timeStep, showplot)
        x0 = np.array(self.getNodesConcentrations(self.refSS))
        x1 = np.array(self.getNodesConcentrations(psol))
        new_response = np.array(2 * (x1 - x0) / (x1 + x0)
                                ).reshape(len(self.nodes), 1)
        self.rglob = np.append(self.rglob, new_response, axis=1)

        # Update the perturbation matrix
        # Set of all species in the module affected by the perturbation
        spc = set()
        if type(par) is list:
            parset = set(par)
        else:
            parset = set([par])
        # Iterate over modules to see which one are affected by perturbations
        for modkey, mod in self.modules.items():
            # Check if at least one parameter in module
            if parset & mod['param']:
                spc.update(mod['species'])
        # Only use species that are nodes
        spc = set.intersection(spc, set(self.nodes))
        # Build the perturbation vector
        new_pert = np.zeros([len(self.nodes), 1], dtype=sympy.Symbol)
        for s in spc:
            indx = self.nodes.index(s)
            new_pert[indx] = sympy.Symbol('rp_' + s)
            # Also keep list of perturbed species
        self.perturbations.append(list(spc))
        # Add to perturbation matrix
        self.rpert_symbols = np.append(self.rpert_symbols, new_pert, axis=1)

    def getNodesConcentrations(self, sssol):
        ndsvals = []
        solasdict = dict(sssol)
        for i in self.nodes:
            ndsvals.append(solasdict[i])
        return np.array(ndsvals)

    def update_refSS(self, showplot=False):
        self.refSS = ssSol(self, showplot=showplot)


###############################################################################
# FUNCTIONS
# These functions are defined within the model's rate laws
# Menten_Explicit_Enzyme = lambda Kcat, E, S, km: Kcat * E * S / (km + S)
# function_0 = lambda kcat, E, S, km: kcat * E * S / (km + S)
# function_1 = lambda v: v
#

# String ordering
# def orderStringsByLength(stringList):
#     """
#     Takes a list of strings and returns a list with the same ids but
#     the longest names are listed before the shorter ones.
#
#     Copied from 'orderGeneNamesByLength' in classifyReactionsByExpression,
#     which is part of EXAMO
#     """
#     # 1. collecting the lengths of all strings
#     lengthSet = set()
#     for name in stringList:
#         lengthSet.add(len(name))
#     # 2. Collecting strings into length `categories'
#     byLengthDict = {}
#     for length in lengthSet:
#         for name in stringList:
#             if length == len(name):
#                 try:
#                     byLengthDict[length].append(name)
#                 except KeyError:
#                     byLengthDict[length] = [name]
#     # 3. Ordering length in descending order
#     lengths = list(byLengthDict.keys())
#     lengths.sort(reverse=True)
#     # 4. creating a list of Ids were long ids preceed shorter ones
#     orderedStringList = []
#     for l in lengths:
#         orderedStringList += byLengthDict[l]
#     return orderedStringList


# Solve system
def ssSol(model, endTime=1e4, timeStep=1, showplot=False):
    """Get the steady state concentration of OdeModelOrton object model.

    Returns list of steady state (species, value) tuples
    [(s1, steady state value of s1),(s2, steady state value of s2),...]

    Inputs:
    model: OdeModelOrton object
    Optional
    endTime (default = 500):  Time integration stops
    timeStep(default = 0.01): Size of iteration step
    """
    simTime = np.arange(0, endTime, timeStep)
    S = model.S
    v = model.rateVector

    def odes(x, t):
        return np.dot(S, v(x))

    # integrating the odes
    tsol = scipy.integrate.odeint(odes, model.init, simTime)
    return list(zip(model.idSp, tsol[-1]))
    # Solving the steady state
    # steady_state = scipy.optimize.fsolve(odes, tsol[-1], (None,))
    # if showplot:
    #    plot_xt(model, tsol, simTime)

    # return list(zip(model.idSp, steady_state))


def kdSol(model, sp, factor, endTime=1e4, timeStep=1, showplot=False):
    """
    Return the steady state of model with species sp knocked-down.

    The original model is not altered/affected.

    Knockdown is modelled by setting the initial concentration of the
    (inactive) species lower by factor.

    Inputs:
    model:  OdeModelOrton object
    sp:     Species name or list of parameter names
    factor: float, factor by which species concentration is reduced.
    Optional
    endTime (default = 500):  Time integration stops
    timeStep(default = 0.1): Size of iteration step
    showplot(default = False): Set True to show time simulations
    """
    perturbedModel = copy.deepcopy(model)
    origInit = model.spDict[sp]['initConcentration']
    perturbedModel.setInit(sp, factor * origInit)
    sol = ssSol(perturbedModel, endTime, timeStep, showplot)
    return sol


def pertSol(model, par, newval, endTime=1e4, timeStep=1, showplot=False):
    """
    Return the steady state of model with parameter par set to value newval.

    The original model is not altered/affected.

    Inputs:
    model:  OdeModelOrton object
    par:    Parameter name or list of parameter names
    newval: New parameter value or list of new parameter values
    Optional
    endTime (default = 500):  Time integration stops
    timeStep(default = 0.1): Size of iteration step
    showplot(default = False): Set True to show time simulations
    """
    perturbedModel = copy.deepcopy(model)
    perturbedModel.setParam(par, newval)
    sol = ssSol(perturbedModel, endTime, timeStep, showplot)
    return sol


def plot_xt(mod, xt, simTime=500):
    # Plotting
    plotSeparately = [9, 11, 18, 25, 30]
    p.subplot(211)
    for i in [j for j in range(len(mod.idSp)) if j not in plotSeparately]:
        p.plot(simTime, xt[:, i])
    p.ylabel('Concentration')

    p.subplot(212)
    for i in plotSeparately:
        p.plot(simTime, xt[:, i])
    p.xlabel('Time')
    p.show()
