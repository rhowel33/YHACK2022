# solutions.py
"""Volume 2: Markov Chains."""

import numpy as np
from scipy import linalg as la
import ctypes




class MarkovChain:
    def __init__(self, A, states=None):
        """Check that A is column stochastic and construct a dictionary
        mapping a state's label to its index (the row / column of A that the
        state corresponds to). Save the transition matrix, the list of state
        labels, and the label-to-index dictionary as attributes.

        Parameters:
        A ((n,n) ndarray): the column-stochastic transition matrix for a
            Markov chain with n states.
        states (list(str)): a list of n labels corresponding to the n states.
            If not provided, the labels are the indices 0, 1, ..., n-1.

        Raises:
            ValueError: if A is not square or is not column stochastic.

        Example:
            >>> MarkovChain(np.array([[.5, .8], [.5, .2]], states=["A", "B"])
        corresponds to the Markov Chain with transition matrix
                                   from A  from B
                            to A [   .5      .8   ]
                            to B [   .5      .2   ]
        and the label-to-index dictionary is {"A":0, "B":1}.
        """
        # Copy A as a NumPy array.
        # A = np.array(A, copy=True)

        # Check that transition matrix is column stochastic.
        m,n = A.shape
        # if m != n:
            # raise ValueError("transition matrix 'A' is not square")
        if not np.allclose(np.ones(n), A.sum(axis=0)):
            raise ValueError("transition matrix 'A' is not column-stochastic")

        # Construct the default state labels if needed.
        if states is None:
            states = list(range(n))
        # if len(states) != n:
            # raise ValueError("shapes of matrix and states not aligned")

        # Save attributes.
        self.A = A
        self.states = states
        self.indices = {state:i for i,state in enumerate(states)}

    # Problem 2
    def transition(self, state):
        """Transition to a new state by making a random draw from the outgoing
        probabilities of the state with the specified label.

        Parameters:
            state (str): the label for the current state.

        Returns:
            (str): the label of the state to transitioned to.
        """
        # Get the index of the current state.
        j = self.indices[state]

        # Get the index of the new state.
        i = np.argmax(np.random.multinomial(1, self.A[:,j]))

        # Return the label corresponding to the new state.
        return self.states[i]

    # Problem 3
    def walk(self, start, N):
        """Starting at the specified state, use the transition() method to
        transition from state to state N-1 times, recording the state label at
        each step.

        Parameters:
            start (str): The starting state label.

        Returns:
            (list(str)): A list of N state labels, including start.
        """
        sequence = [start]
        current_state = start
        for _ in range(N-1):                # Transition N-1 times.
            current_state = self.transition(current_state)
            sequence.append(current_state)

        return sequence

    # Problem 3
    def path(self, start, stop):
        """Beginning at the start state, transition from state to state until
        arriving at the stop state, recording the state label at each step.

        Parameters:
            start (str): The starting state label.
            stop (str): The stopping state label.

        Returns:
            (list(str)): A list of state labels from start to stop.
        """
        sequence = [start]
        current_state = start
        while current_state != stop:        # Transition until finding stop.
            current_state = self.transition(current_state)
            sequence.append(current_state)

        return sequence

    # Problem 4
    def steady_state(self, tol=1e-12, maxiter=40):
        """Compute the steady state of the transition matrix A.

        Parameters:
            tol (float): The convergence tolerance.
            maxiter (int): The maximum number of iterations to compute.

        Returns:
            ((n,) ndarray): The steady state distribution vector of A.

        Raises:
            ValueError: if there is no convergence within maxiter iterations.
        """
        # Generate a random initial state distribution vector.
        x0 = np.random.random(self.A.shape[0])
        x0 /= x0.sum()

        # Iteration until convergence or until iterating maxiters times.
        for i in range(maxiter):
            x1 = self.A @ x0
            if la.norm(x0 - x1, ord=1) < tol:
                return x1
            x0 = x1

        raise ValueError("maximum number of iterations exceeded")

class SentenceGenerator(MarkovChain):
    """A Markov-based simulator for natural language.

    Attributes:
        A ((n,n) ndarray): the column-stochastic transition matrix for a
            Markov chain with n states, constructed from a file.
        states (list(str)): a list of n labels corresponding to the n states.
            If not provided, the labels are the indices 0, 1, ..., n-1.
        indices (dict(str -> int)): a dictionary mapping a state's label to
            its index, i.e., column indices[L] of A corresponds to state L.
    """
    # Problem 5
    def __init__(self, filename):
        """Read the specified file and build a transition matrix from its
        contents. You may assume that the file has one complete sentence
        written on each line.
        """
        # Read the file.
        with open(filename, 'r') as infile:
            data = infile.read()

        # Get all of the unique states, plus start and stop states.
        states = ["$tart"] + list(set(data.split())) + ["$top"]

        # Construct the state label indicies and the empty transition matrix.
        num_states = len(states)
        indices = {state:i for i,state in enumerate(states)}
        A = np.zeros((num_states, num_states))

        # Get the transition probabilities, assuming one sentence per line.
        for line in data.split('\n'):
            sentence = ["$tart"] + line.split() + ["$top"]
            for before, after in zip(sentence[:-1], sentence[1:]):
                A[indices[after], indices[before]] += 1

        stopindex = indices["$top"]
        A[stopindex, stopindex] = 1.

        # Normalize the columns of the transition matrix so they sum to 1.
        A /= A.sum(axis=0)

        # Store attributes.
        self.A = A
        self.states = states
        self.indices = indices
        # self.filename = filename

    # Problem 6
    def babble(self,):
        """Create a random sentence using MarkovChain.path().

        Returns:
            sentence (str): A sentence generated with the transition matrix,
                not including the labels for the $tart and $top states.

        Example:
            >>> yoda = SentenceGenerator("yoda.txt")
            >>> print(yoda.babble())
            The dark side of loss is a path as one with you.
        """

        return " ".join(self.path("$tart", "$top")[1:-1])


class NGRAM:
    def __init__(self,N,filename='kevin.txt'):
        self.N = N
        self.file = filename
        self.words = []
        self.vocabulary = set()
        self. wordmap = {}
        self.temp = None
        self.nopunct = None
        self.state = []
        self.rng = np.random.default_rng()

    def fit(self):
        PUNCT = [',', '.', ';', ':', '!', '?']
        START =  '<START>'
        STOP = '<STOP>'

        with open(self.file) as fin:
            data = fin.read().split(' ')


        for word in data:
            self.nopunct = ''
            punct_flag = False

            for char in word:
                punct_char = ''
                if char.isalpha():
                    self.nopunct+=char
                else:
                    for punc in PUNCT:
                        punct_char += punc
                        punct_flag = True
                        break
                    if punct_flag:
                        self.words.append(self.nopunct)
                        self.words.append(punct_char)

                break

            if not punct_flag:
                self.words.append(self.nopunct)

        for i in range(self.N):
            self.state.append(START)

        for word in self.words:
            try:
                self.wordmap[' '.join(self.state)].append(word)
            except KeyError:
                self.wordmap[' '.join(self.state)] = [word]
            self.state.append(word)
            self.state = self.state[1:]

        try:
            self.wordmap[' '.join(self.state)].append(STOP)
        except KeyError:
            self.wordmap[' '.join(self.state)] = [STOP]

    def predict(self):
        state = ' '.join(START for _ in range(self.N))
        while not self.stop():
            no_space_flag = False
            index = self.rng.normal()


if __name__ == "__main__":
    nmf = NGRAM(3)
    nmf.fit()



