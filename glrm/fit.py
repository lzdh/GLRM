from math import sqrt

class Block(object):
    # FYI: we use (X, Y) here but sometimes it's (Y, X)
    # For each alternating minimization step, the first term is the parameter
    # and the second term is the optimization variable.

    def __init__(self, loss, reg = None):
        if not isinstance(loss, list): loss = [loss]
        self.L = loss
        self.r = reg

    def __str__(self):
        return "{0} + {1}".format(str(self.L), str(self.r))

    def __call__(self, Xs, Y):
        # Return objective value of rows (or cols) evalulated at X, Y
        if not isinstance(Xs, list): Xs = [Xs]
        return sum([L(X, Y) for L, X in zip(self.L, Xs)])

    def update(self, Xs, Y, converge, skip_last_col = False):
        # gradient descent step
        # to implement more algorithms, refer to old code
        if not isinstance(Xs, list): Xs = [Xs]
        alpha = 0.001 # XXX stepsize 
        
        while not converge.d():
            # gradient step
            grad = sum([L.subgrad(X, Y) for L, X in zip(self.L, Xs)])
            grad_r = self.r.subgrad(Y)
            if skip_last_col:
                grad_r[-1:,:] = 0
                grad[-1:,:] = 0
            Y -= alpha/sqrt(len(converge)+1)*(grad + grad_r)

            # update convergence object
            converge.val.append(Y)
            converge.obj.append(self(Xs, Y)) 