r"""
Fully packed loops

A class for fully packed loops [Propp2001]_.
We can create a fully packed loop using the corresponding alternating sign matrix::

    sage: A = AlternatingSignMatrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    sage: fpl = FullyPackedLoop(A)
    sage: fpl
        |         |
        |         |
        # -- #    #
             |    |
             |    |
     -- #    #    # --
        |    |
        |    |
        #    # -- #
        |         |
        |         |

The class also has a plot method::

    sage: fpl.plot()
    Graphics object consisting of 15 graphics primitives

which gives:

.. PLOT::
    :width: 200 px

    A = AlternatingSignMatrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
    fpl = FullyPackedLoop(A)
    p = fpl.plot()
    sphinx_plot(p)

Note that we can also create a fully packed loop from a six vertex model configuration::

    sage: S = SixVertexModel(3, boundary_conditions='ice').from_alternating_sign_matrix(A)
    sage: S
        ^    ^    ^
        |    |    |
    --> # -> # -> # <--
        ^    ^    |
        |    |    V
    --> # -> # <- # <--
        ^    |    |
        |    V    V
    --> # <- # <- # <--
        |    |    |
        V    V    V
    sage: fpl = FullyPackedLoop(S)
    sage: fpl
        |         |
        |         |
        # -- #    #
             |    |
             |    |
     -- #    #    # --
        |    |
        |    |
        #    # -- #
        |         |
        |         |

Once we have a fully packed loop we can obtain the corresponding alternating sign matrix::

    sage: fpl.to_alternating_sign_matrix()
    [0 0 1]
    [0 1 0]
    [1 0 0]

REFERENCES:

.. [Propp2001] James Propp.
   *The Many Faces of Alternating Sign Matrices*
   Discrete Mathematics and Theoretical Computer Science 43 (2001): 58
"""
from sage.structure.sage_object import SageObject
from sage.combinat.six_vertex_model import SquareIceModel, SixVertexConfiguration
from sage.combinat.alternating_sign_matrix import AlternatingSignMatrix
from sage.plot.graphics import Graphics
from sage.plot.line import line


class FullyPackedLoop(SageObject):
    """
    A class for fully packed loops
    """

    def __init__(self, generator):
        """
        Initialise object: what are we going to use as generators? Perhaps multiple: ASM, and Six Vertex Model

        EXAMPLES:

        We can initiate a fully packed loop using an Alternating Sign Matrix::

            sage: A = AlternatingSignMatrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
            sage: fpl = FullyPackedLoop(A)
            sage: fpl
                |         |
                |         |
                # -- #    #
                     |    |
                     |    |
             -- #    #    # --
                |    |
                |    |
                #    # -- #
                |         |
                |         |

        Otherwise we initiate a fully packed loop using a six vertex model::

            sage: S = SixVertexModel(3, boundary_conditions='ice').from_alternating_sign_matrix(A)
            sage: fpl = FullyPackedLoop(S)
            sage: fpl
                |         |
                |         |
                # -- #    #
                     |    |
                     |    |
             -- #    #    # --
                |    |
                |    |
                #    # -- #
                |         |
                |         |
            sage: fpl.six_vertex_model.to_alternating_sign_matrix()
            [0 0 1]
            [0 1 0]
            [1 0 0]

        Note that if anything else is used to generate the fully packed loop an error will occur::

            sage: fpl = FullyPackedLoop(5)
            Traceback (most recent call last):
            ...
            TypeError: The generator for a fully packed loop must either be an AlternatingSignMatrix or a SixVertexConfiguration

            sage: fpl = FullyPackedLoop((1, 2, 3))
            Traceback (most recent call last):
            ...
            TypeError: The generator for a fully packed loop must either be an AlternatingSignMatrix or a SixVertexConfiguration

        """
        if isinstance(generator, AlternatingSignMatrix):
            self.six_vertex_model = generator.to_six_vertex_model()
        elif isinstance(generator, SixVertexConfiguration):
            self.six_vertex_model = generator
        else:
            raise TypeError('The generator for a fully packed loop must either be an AlternatingSignMatrix or a SixVertexConfiguration')

    def _repr_(self):
        """
        Return a string representation of ``self``.

        EXAMPLES::

            sage: A = AlternatingSignMatrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            sage: fpl = FullyPackedLoop(A)
            sage: fpl
                |         |
                |         |
                #    # -- #
                |    |
                |    |
             -- #    #    # --
                     |    |
                     |    |
                # -- #    #
                |         |
                |         |

            sage: A = AlternatingSignMatrix([[0,1,0,0],[0,0,1,0],[1,-1,0,1],[0,1,0,0]])
            sage: S = SixVertexModel(4, boundary_conditions='ice').from_alternating_sign_matrix(A)
            sage: fpl = FullyPackedLoop(S)
            sage: fpl
                |         |
                |         |
                # -- # -- #    # --
                               |
                               |
             -- #    # -- # -- #
                |    |
                |    |
                #    #    # -- # --
                |    |    |
                |    |    |
             -- #    #    # -- #
                     |         |
                     |         |

        """
        # List are in the order of URDL
        # One set of rules for how to draw around even vertex, one set of rules for odd vertex
        n=len(self.six_vertex_model)-1
        ascii1 = [[r'     ', ' -', r'     ', '- '], # LR
                 [r'  |  ', '  ', r'     ', '- '], # LU
                 [r'     ', '  ', r'  |  ', '- '], # LD
                 [r'  |  ', '  ', r'  |  ', '  '], # UD
                 [r'  |  ', ' -', r'     ', '  '], # UR
                 [r'     ', ' -', r'  |  ', '  ']] # RD

        ascii2 = [[r'  |  ', '  ', r'  |  ', '  '], # LR
                 [r'     ', ' -', r'  |  ', '  '], # LU
                 [r'  |  ', ' -', r'     ', '  '], # LD
                 [r'     ', ' -', r'     ', '- '], # UD
                 [r'     ', '  ', r'  |  ', '- '], # UR
                 [r'  |  ', '  ', r'     ', '- ']] # RD
        ret = '  '
        # Do the top line
        for i,entry in enumerate(self.six_vertex_model[0]):
            if i % 2 == 0:
                ret += '  |  '
            else:
                ret += '     '
#            if entry == 1 or entry == 3 or entry == 4:
#                ret += '  ^  '
#            else:
#                ret += '  |  '

        # Do the meat of the ascii art
        for j,row in enumerate(self.six_vertex_model):
            ret += '\n  '
            # Do the top row
            for i,entry in enumerate(row):
                if (i+j) % 2 == 0:
                    ret += ascii1[entry][0]
                else:
                    ret += ascii2[entry][0]
            ret += '\n'

            # Do the left-most entry
            if (j) % 2 == 0:
                ret += '  '
            else:
                ret += ' -'

            # Do the middle row
            for i,entry in enumerate(row):
                if (i+j) % 2 == 0:
                    ret += ascii1[entry][3] + '#' + ascii1[entry][1]
                else:
                    ret += ascii2[entry][3] + '#' + ascii2[entry][1]

            # Do the right-most entry
            if (j+n) % 2 ==0:
                ret += '  '
            else:
                ret += '- '

            # Do the bottom row
            ret += '\n  '
            for i,entry in enumerate(row):
                if (i+j) % 2 ==0:
                    ret += ascii1[entry][2]
                else:
                    ret += ascii2[entry][2]

        # Do the bottom line
        ret += '\n  '
        for i,entry in enumerate(self.six_vertex_model[-1]):
            if (i+n+1) % 2 ==0:
                ret += '     '
            else:
                ret += '  |  '



#            if entry == 2 or entry == 3 or entry == 5:
#                ret += '  V  '
#            else:
#                ret += '  |  '

        return ret

    def to_alternating_sign_matrix(self):
        """

        Returns the alternating sign matrix corresponding to this class.

         EXAMPLES::

            sage: A = AlternatingSignMatrix([[0, 1, 0], [1, -1, 1], [0, 1, 0]])
            sage: S = SixVertexModel(3, boundary_conditions='ice').from_alternating_sign_matrix(A)
            sage: fpl = FullyPackedLoop(S)
            sage: fpl.to_alternating_sign_matrix()
            [ 0  1  0]
            [ 1 -1  1]
            [ 0  1  0]
            sage: A = AlternatingSignMatrix([[0,1,0,0],[0,0,1,0],[1,-1,0,1],[0,1,0,0]])
            sage: S = SixVertexModel(4, boundary_conditions='ice').from_alternating_sign_matrix(A)
            sage: fpl = FullyPackedLoop(S)
            sage: fpl.to_alternating_sign_matrix()
            [ 0  1  0  0]
            [ 0  0  1  0]
            [ 1 -1  0  1]
            [ 0  1  0  0]
        """
        return self.six_vertex_model.to_alternating_sign_matrix()


    def plot(self):
        """
        Return a graphical object of the Fully Packed Loop

        EXAMPLES:

        Here is the fully packed for :math:`\\begin{pmatrix}0&1&1\\\\1&-1&1\\\\0&1&0\end{pmatrix}`:

        .. PLOT::
            :width: 200 px

            A = AlternatingSignMatrix([[0, 1, 0], [1, -1, 1], [0, 1, 0]])
            fpl = FullyPackedLoop(A)
            p = fpl.plot()
            sphinx_plot(p)

        Here is how Sage represents this::

            sage: A = AlternatingSignMatrix([[0, 1, 0], [1, -1, 1], [0, 1, 0]])
            sage: fpl = FullyPackedLoop(A)
            sage: print fpl.plot().description()
            Line defined by 2 points:       [(-1.0, 1.0), (0.0, 1.0)]
            Line defined by 2 points:       [(0.0, 0.0), (0.0, -1.0)]
            Line defined by 2 points:       [(0.0, 0.0), (1.0, 0.0)]
            Line defined by 2 points:       [(0.0, 2.0), (0.0, 3.0)]
            Line defined by 2 points:       [(0.0, 2.0), (0.0, 3.0)]
            Line defined by 2 points:       [(0.0, 2.0), (1.0, 2.0)]
            Line defined by 2 points:       [(1.0, 1.0), (0.0, 1.0)]
            Line defined by 2 points:       [(1.0, 1.0), (2.0, 1.0)]
            Line defined by 2 points:       [(2.0, 0.0), (1.0, 0.0)]
            Line defined by 2 points:       [(2.0, 0.0), (2.0, -1.0)]
            Line defined by 2 points:       [(2.0, 2.0), (1.0, 2.0)]
            Line defined by 2 points:       [(2.0, 2.0), (2.0, 3.0)]
            Line defined by 2 points:       [(2.0, 2.0), (2.0, 3.0)]
            Line defined by 2 points:       [(3.0, 1.0), (2.0, 1.0)]
            Line defined by 2 points:       [(3.0, 1.0), (2.0, 1.0)]

        Here are the other 3 by 3 Alternating Sign Matrices and their corresponding fully packed loops:

        .. math::

            A = \\begin{pmatrix}
                1&0&0\\\\
                0&1&0\\\\
                0&0&1\\\\
                \end{pmatrix}

        gives:

        .. PLOT::
            :width: 200 px

            A = AlternatingSignMatrix([[1, 0, 0], [0, 1, 0], [0, 0, 1]])
            fpl = FullyPackedLoop(A)
            p = fpl.plot()
            sphinx_plot(p)

        .. math::

            A = \\begin{pmatrix}
                1&0&0\\\\
                0&0&1\\\\
                0&1&0\\\\
                \end{pmatrix}

        gives:

        .. PLOT::
            :width: 200 px

            A = AlternatingSignMatrix([[1, 0, 0], [0, 0, 1], [0, 1, 0]])
            fpl = FullyPackedLoop(A)
            p = fpl.plot()
            sphinx_plot(p)

        .. math::

            A = \\begin{pmatrix}
                0&1&0\\\\
                1&0&0\\\\
                0&0&1\\\\
                \end{pmatrix}

        gives:

        .. PLOT::
            :width: 200 px

            A = AlternatingSignMatrix([[0, 1, 0], [1, 0, 0], [0, 0, 1]])
            fpl = FullyPackedLoop(A)
            p = fpl.plot()
            sphinx_plot(p)

        .. math::

            A = \\begin{pmatrix}
                0&1&0\\\\
                0&0&1\\\\
                1&0&0\\\\
                \end{pmatrix}

        gives:

        .. PLOT::
            :width: 200 px

            A = AlternatingSignMatrix([[0, 1, 0], [0, 0, 1], [1, 0, 0]])
            fpl = FullyPackedLoop(A)
            p = fpl.plot()
            sphinx_plot(p)

        .. math::

            A = \\begin{pmatrix}
                0&0&1\\\\
                1&0&0\\\\
                0&1&0\\\\
                \end{pmatrix}

        gives:

        .. PLOT::
            :width: 200 px

            A = AlternatingSignMatrix([[0, 0, 1], [1, 0, 0], [0, 1, 0]])
            fpl = FullyPackedLoop(A)
            p = fpl.plot()
            sphinx_plot(p)

        .. math::

            A = \\begin{pmatrix}
                0&0&1\\\\
                0&1&0\\\\
                1&0&0\\\\
                \end{pmatrix}

        gives:

        .. PLOT::
            :width: 200 px

            A = AlternatingSignMatrix([[0, 0, 1], [0, 1, 0], [1, 0, 0]])
            fpl = FullyPackedLoop(A)
            p = fpl.plot()
            sphinx_plot(p)

        EXAMPLES::

                sage: A = AlternatingSignMatrix([[0, 1, 0, 0], [1, -1, 0, 1], [0, 1, 0, 0],[0, 0, 1, 0]])
                sage: fpl = FullyPackedLoop(A)
                sage: print fpl.plot().description()
                Line defined by 2 points:       [(-1.0, 0.0), (0.0, 0.0)]
                Line defined by 2 points:       [(-1.0, 2.0), (0.0, 2.0)]
                Line defined by 2 points:       [(0.0, 1.0), (0.0, 0.0)]
                Line defined by 2 points:       [(0.0, 1.0), (1.0, 1.0)]
                Line defined by 2 points:       [(0.0, 3.0), (0.0, 4.0)]
                Line defined by 2 points:       [(0.0, 3.0), (0.0, 4.0)]
                Line defined by 2 points:       [(0.0, 3.0), (1.0, 3.0)]
                Line defined by 2 points:       [(1.0, 0.0), (1.0, -1.0)]
                Line defined by 2 points:       [(1.0, 0.0), (2.0, 0.0)]
                Line defined by 2 points:       [(1.0, 2.0), (0.0, 2.0)]
                Line defined by 2 points:       [(1.0, 2.0), (2.0, 2.0)]
                Line defined by 2 points:       [(2.0, 1.0), (1.0, 1.0)]
                Line defined by 2 points:       [(2.0, 1.0), (2.0, 2.0)]
                Line defined by 2 points:       [(2.0, 3.0), (1.0, 3.0)]
                Line defined by 2 points:       [(2.0, 3.0), (2.0, 4.0)]
                Line defined by 2 points:       [(2.0, 3.0), (2.0, 4.0)]
                Line defined by 2 points:       [(3.0, 0.0), (2.0, 0.0)]
                Line defined by 2 points:       [(3.0, 0.0), (3.0, -1.0)]
                Line defined by 2 points:       [(3.0, 2.0), (3.0, 1.0)]
                Line defined by 2 points:       [(3.0, 2.0), (3.0, 3.0)]
                Line defined by 2 points:       [(4.0, 1.0), (3.0, 1.0)]
                Line defined by 2 points:       [(4.0, 1.0), (3.0, 1.0)]
                Line defined by 2 points:       [(4.0, 3.0), (3.0, 3.0)]
                Line defined by 2 points:       [(4.0, 3.0), (3.0, 3.0)]

        Here is the plot:

        .. PLOT::
            :width: 300 px

            A = AlternatingSignMatrix([[0, 1, 0, 0], [1, -1, 0, 1], [0, 1, 0, 0],[0, 0, 1, 0]])
            fpl = FullyPackedLoop(A)
            p = fpl.plot()
            sphinx_plot(p)

        """
        G = Graphics()
        n=len(self.six_vertex_model)-1
        for j,row in enumerate(reversed(self.six_vertex_model)):
            for i,entry in enumerate(row):
                if i == 0 and (i+j+n+1) % 2 ==0:
                    G+= line([(i-1,j),(i,j)])
                if i == n and (i+j+n+1) % 2 ==0:
                    G+= line([(i+1,j),(i,j)])
                if j == 0 and (i+j+n) % 2 ==0:
                    G+= line([(i,j),(i,j-1)])
                if j == n and (i+j+n) % 2 ==0:
                    G+= line([(i,j),(i,j+1)])
                if entry == 0: # LR
                    if (i+j+n) % 2==0:
                        G += line([(i,j), (i+1,j)])
                    else:
                        G += line([(i,j),(i,j+1)])
                elif entry == 1: # LU
                    if (i+j+n) % 2 ==0:
                        G += line([(i,j), (i,j+1)])
                    else:
                        G += line([(i+1,j), (i,j)])
                elif entry == 2: # LD
                    if (i+j+n) % 2 == 0:
                        pass
                    else:
                        G += line([(i,j+1), (i,j)])
                        G += line([(i+1,j), (i,j)])
                elif entry == 3: # UD
                    if (i+j+n) % 2 == 0:
                        G += line([(i,j), (i,j+1)])
                    else:
                        G += line([(i+1,j), (i,j)])
                elif entry == 4: # UR
                    if (i+j+n) % 2 ==0:
                        G += line([(i,j), (i,j+1)])
                        G += line([(i,j), (i+1,j)])
                    else:
                        pass
                elif entry == 5: # RD
                    if (i+j+n) % 2 ==0:
                        G += line([(i,j), (i+1,j)])
                    else:
                        G += line([(i,j+1), (i,j)])
        G.axes(False)
        return G

        def link_pattern(self):
            """
            Return a :class:`PerfectMatching` class (a non-crossing partition) corresponding to a fully packed loop.
            Note: by convention, we choose the top left vertex to be even. See [Propp2001]_.

            EXAMPLES:

            We can extract the underlying link pattern (a non-crossing partition) from a fully packed loop::
     
                sage: A = AlternatingSignMatrix([[0, 1, 0], [1, -1, 1], [0, 1, 0]])
                sage: fpl = FullyPackedLoop(A)
                sage: fpl.link_pattern()
                [(1, 2), (3, 6), (4, 5)]
            """
            link_pattern=[]
            svm = self.six_vertex_model
            n=len(svm)

            # dictionary of vertices - endpoint
            vertices = {}
            for i in range(n):
                for j in range(n):
                    vertices[(i, j)] = 0

            end_points = {}

            for k in range(n):
                if k % 2 == 0:
                    # top row
                    vertices[(0, k)] = 1 + k/2
                    end_points[1 + k/2] = (0, k)

                    # bottom row
                    vertices[(n, n-k)] = n + 1 + k/2
                    end_points[n + 1 + k/2] = (n, n-k)

            # sides for even case
            if n % 2 == 0:
                for k in range(n):
                    if k % 2 == 0:
                        # left side
                        vertices[(n-k, 0)] = (3*n + 2 + k)/2
                        end_points[((3*n + 2 + k)/2)] = (n-k, 0)
                        # right side
                        vertices[(k, n)] = (n + 2 + k)/2
                        end_points[(n + 2 + k)/2] = (k, n)

            # side for odd case
            if n % 2 == 1:
                for k in range(n):
                    if k % 2 == 1:
                        # left side
                        vertices[(n-k, 0)] = (3*n + 2 + k)/2
                        end_points[(3*n + 2 + k)/a2] = (n-k, 0)
                        # right side
                        vertices[(k, n)] = (n + 2 + k)/2
                        end_points[(n + 2 + k)/2] = (k, n)
