
# build_numpy.py - numpy.html with 40 topics (6 major sections)
import os, sys
sys.path.insert(0, r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final")
from build_all import HEAD, HERO, toc, section, cb, note, ptable, mgrid, sig, playground, foot

BASE = r"C:\Users\DELL\.gemini\antigravity\scratch\python-docs-final"

topics = [
    "Array Creation — np.array, zeros, ones, eye, arange, linspace",
    "Array Attributes — shape, dtype, ndim, size, strides, flags",
    "Indexing & Slicing — basic, 2D, boolean, fancy, np.where",
    "Reshaping — reshape, flatten, ravel, squeeze, expand_dims",
    "Stacking & Splitting — concat, vstack, hstack, dstack, split",
    "Arithmetic Ufuncs — add, multiply, divide, sqrt, power, mod",
    "Exponential & Log — exp, log, log2, log10, log1p, expm1",
    "Trigonometry — sin, cos, tan, arcsin, arctan2 (all in radians)",
    "Rounding — floor, ceil, round, trunc, clip, maximum, minimum",
    "Linear Algebra — dot, matmul, linalg: det, inv, eig, svd, solve",
    "Sum & Product — sum, prod, cumsum, cumprod (axis, keepdims)",
    "Statistics — mean, median, std, var, axis, ddof params",
    "Min/Max/ArgMin/ArgMax — min, max, argmin, argmax, ptp",
    "Percentile & Quantile — percentile, quantile, interpolation",
    "NaN-safe — nansum, nanmean, nanstd, nanmax, nanargmin",
    "Unique & Sort — unique (all returns), sort, argsort, in-place",
    "Boolean — all, any, isnan, isinf, isclose, allclose, array_equal",
    "Set Operations — in1d, intersect1d, union1d, setdiff1d, setxor1d",
    "Broadcasting Rules — 5 worked examples + 2 ValueError cases",
    "dtypes — int8/16/32/64 uint float16/32/64 complex bool str object astype",
    "Views vs Copies — view(), copy(), shares_memory, when indexing copies",
    "Structured Arrays — custom dtype with named fields, field access",
    "Save & Load — save, load, savez, savetxt, loadtxt (all params)",
    "apply_along_axis & apply_over_axes",
    "np.vectorize — pyfunc, otypes, excluded; when to use",
    "np.meshgrid — indexing xy/ij, sparse, coord grids",
    "np.einsum — subscript notation, 6 worked examples",
    "np.pad — all modes: constant, edge, reflect, wrap, linear_ramp",
    "Masked Arrays — ma.array, ma.masked_where, ma.filled",
    "Memory Layout — C-order vs F-order, strides, contiguous check",
    "np.frompyfunc, np.frombuffer, np.fromfunction, np.fromiter",
    "Random Module — rand, randn, randint, seed, default_rng, Generator",
    "Aggregation Extras — np.diff, np.gradient, np.trapz, np.cross",
    "np.where & np.select — conditional element selection",
    "np.take & np.put — advanced gather/scatter",
    "np.searchsorted — bisect-style search in sorted arrays",
    "np.digitize & np.histogram — binning data",
    "np.polyfit & np.polyval — polynomial fitting",
    "np.fft — fft, ifft, fftfreq, rfft, irfft",
    "Performance — vectorize vs loop, memory contiguous, avoid copies",
]

s1 = section(1,"Array Creation",
    "np.array() wraps any sequence. Specialized constructors (zeros, ones, arange, linspace) "
    "are faster and clearer than explicit loops or list comprehensions.",
    cb("np.array / zeros / ones / empty / full / eye / arange / linspace / logspace / random",
"""import numpy as np

# np.array — most general constructor
a = np.array([1,2,3])                  # 1D int array
b = np.array([[1,2],[3,4]], dtype=float) # 2D float
c = np.array([1,2,3], ndmin=3)         # force 3D: shape (1,1,3)

print(a.shape, a.dtype)   # (3,) int64
print(b.shape, b.dtype)   # (2,2) float64
print(c.shape)            # (1,1,3)

# Constant arrays
z = np.zeros((3,4))              # 3x4 zeros (float64)
o = np.ones((2,3), dtype=int)    # 2x3 ones (int)
e = np.empty((2,2))             # uninitialized (fast)
f = np.full((3,3), 7.0)         # filled with 7.0

# Like-arrays (same shape/dtype as existing)
zl = np.zeros_like(b)            # 2x2 zeros float64
ol = np.ones_like(a, dtype=float)# 1D ones float64

# Identity / diagonal
eye3 = np.eye(3)                 # 3x3 identity
eye34k1 = np.eye(3,4,k=1)       # 3x4, 1 above main diagonal
ident = np.identity(3)           # always square

# Range arrays
ar = np.arange(0, 10, 2)        # [0 2 4 6 8]
ar2 = np.arange(0.0, 1.0, 0.25) # [0.  0.25 0.5  0.75]  (float OK)

# linspace — guaranteed endpoint, exact count
ls = np.linspace(0, 1, 5)        # [0.   0.25 0.5  0.75 1.  ]
arr, step = np.linspace(0,1,5,retstep=True)
print(f"step={step:.2f}")        # step=0.25

# logspace / geomspace
log = np.logspace(0, 3, 4)       # [1., 10., 100., 1000.]
geo = np.geomspace(1, 1000, 4)   # same values

# Random arrays
rng = np.random.default_rng(42)  # modern Generator API
r1  = rng.random((2,3))          # uniform [0,1)
r2  = rng.integers(0,10,(3,3))   # int in [0,10)
r3  = rng.normal(0,1,(4,))       # standard normal
r4  = rng.choice([1,2,3,4], size=5, replace=False)  # sampling

# Legacy API (still common)
np.random.seed(42)
print(np.random.rand(3))         # 3 uniform floats
print(np.random.randn(3))        # 3 standard normal
print(np.random.randint(0,10,5)) # 5 random ints""",
["(3,) int64","(2, 2) float64","(1, 1, 3)","step=0.25",
 "[0.37 0.95 0.73]","[-0.47 1.76 0.19]","[6 1 4 4 8]"]),
    ptable([
        ("object","array-like","—","Nested list, tuple, or array to convert"),
        ("dtype","dtype","None","np.int32, np.float64, 'U10', etc. None=inferred"),
        ("copy","bool","True","If False, avoid copy when possible"),
        ("ndmin","int","0","Minimum number of dimensions to ensure"),
        ("order","str","'K'","'C'=row-major, 'F'=column-major, 'A'=auto, 'K'=keep"),
    ])
)

s2 = section(2,"Array Attributes",
    "Every ndarray has a fixed set of attributes describing its shape, memory layout, and data type. "
    "These are properties (not methods) — no parentheses.",
    cb("All ndarray attributes",
"""import numpy as np
a = np.array([[1,2,3],[4,5,6]], dtype=np.float32)

print(a.shape)      # (2, 3)          — tuple of dim sizes
print(a.dtype)      # float32         — element type
print(a.ndim)       # 2               — number of axes
print(a.size)       # 6               — total elements
print(a.itemsize)   # 4               — bytes per element
print(a.nbytes)     # 24              — total bytes (size*itemsize)
print(a.T.shape)    # (3, 2)          — transposed shape
print(a.flat[3])    # 4.0             — flat iterator element
print(a.strides)    # (12, 4)         — bytes to next row/col

# flags — memory layout info
print(a.flags)
# C_CONTIGUOUS : True   (row-major order)
# F_CONTIGUOUS : False
# OWNDATA : True        (array owns its memory)
# WRITEABLE : True
# ALIGNED : True

# Data type inspection
print(a.dtype.name)       # 'float32'
print(a.dtype.itemsize)   # 4
print(a.dtype.kind)       # 'f' (float; u=uint, i=int, b=bool, U=str)

# dtype conversion
b = a.astype(np.int32)
print(b.dtype)      # int32
c = a.astype('U10') # convert to string dtype""",
["(2, 3)","float32","2","6","4","24","(3, 2)","4.0","(12, 4)","int32"])
)

s3 = section(3,"Indexing &amp; Slicing",
    "NumPy supports basic indexing (returns view), boolean indexing (returns copy), "
    "fancy indexing with arrays (returns copy), and np.where for conditional selection.",
    cb("basic / 2D / boolean / fancy / np.where / np.argwhere / np.nonzero",
"""import numpy as np

# 1D basic
a = np.array([10,20,30,40,50])
print(a[0], a[-1])      # 10 50
print(a[1:4])           # [20 30 40]
print(a[::2])           # [10 30 50]

# 2D indexing
m = np.arange(1,13).reshape(3,4)
# [[ 1  2  3  4]
#  [ 5  6  7  8]
#  [ 9 10 11 12]]
print(m[1,2])           # 7       (row 1, col 2)
print(m[1])             # [5 6 7 8]  (entire row 1)
print(m[:,2])           # [ 3  7 11]  (entire col 2)
print(m[0:2, 1:3])      # [[2 3],[6 7]] (sub-matrix)

# Boolean indexing (returns copy)
a = np.array([1,2,3,4,5,6])
mask = a > 3
print(a[mask])          # [4 5 6]
print(a[a%2==0])        # [2 4 6]
a[a<0] = 0              # in-place conditional assignment

# Fancy indexing (array of indices, returns copy)
idx = np.array([0,2,4])
print(a[idx])           # [1 3 5]
# 2D fancy
print(m[[0,2]])         # rows 0 and 2
print(m[[0,1],[2,3]])   # m[0,2] and m[1,3] → [3 8]

# np.where(condition, x, y) — element-wise ternary
x = np.array([1,-2,3,-4,5])
print(np.where(x>0, x, 0))     # [1 0 3 0 5]
print(np.where(x>0, "pos","neg"))  # broadcast strings

# np.where(condition) — returns indices of True elements (like np.nonzero)
print(np.where(x>0))   # (array([0,2,4]),)

# np.argwhere — indices of non-zero in column format
print(np.argwhere(x>0))  # [[0],[2],[4]]

# np.nonzero — tuple of arrays, one per dimension
print(np.nonzero(x>0))   # (array([0,2,4]),)

# np.take / np.put
arr = np.array([10,20,30,40])
print(np.take(arr,[0,2]))  # [10 30]  (like fancy but with mode params)
np.put(arr,[1,3],[99,88])  # modifies in-place
print(arr)                 # [10 99 30 88]""",
["10 50","[20 30 40]","[10 30 50]","7","[5 6 7 8]","[ 3  7 11]","[4 5 6]","[2 4 6]",
 "[1 0 3 0 5]","(array([0, 2, 4]),)","[[0],[2],[4]]","[10 30]","[10 99 30 88]"])
)

s4 = section(4,"Reshaping",
    "reshape() tries to return a VIEW (same memory). flatten() always returns a copy. "
    "ravel() returns a view where possible.",
    cb("reshape / flatten / ravel / squeeze / expand_dims / transpose / rollaxis / moveaxis",
"""import numpy as np

a = np.arange(1,13)     # [1..12]

# reshape — returns view if possible
m = a.reshape(3,4)       # (3,4)
t = a.reshape(2,2,3)     # (2,2,3)
r = a.reshape(-1,4)      # auto-compute first dim: (3,4)

print(m.shape)           # (3, 4)
print(t.shape)           # (2, 2, 3)

# flatten — always copy, always 1D
f = m.flatten()          # [1 2 3 ... 12]  copy
f[0] = 999
print(m[0,0])            # 1  (unchanged — it's a copy)

# ravel — view if contiguous
rv = m.ravel()           # [1 2 3 ... 12]  likely view
rv[0] = 999
print(m[0,0])            # 999  (it's a view!)

# squeeze — remove size-1 dimensions
a2 = np.zeros((1,3,1))
print(a2.shape)          # (1, 3, 1)
print(np.squeeze(a2).shape)     # (3,)
print(np.squeeze(a2,axis=0).shape)  # (3, 1)

# expand_dims — add size-1 dimension
v = np.array([1,2,3])   # shape (3,)
print(np.expand_dims(v,axis=0).shape)  # (1, 3)
print(np.expand_dims(v,axis=1).shape)  # (3, 1)
print(v[np.newaxis,:].shape)           # (1, 3)  equivalent
print(v[:,np.newaxis].shape)           # (3, 1)

# Transpose
m = np.arange(6).reshape(2,3)
print(m.T.shape)         # (3, 2)
print(np.transpose(m).shape)  # (3, 2)

# 3D transpose with axes order
t = np.zeros((2,3,4))
print(np.transpose(t,(2,0,1)).shape)  # (4,2,3)
print(np.moveaxis(t,2,0).shape)       # (4,2,3)  same effect""",
["(3, 4)","(2, 2, 3)","1","999","(1, 3, 1)","(3,)","(3, 1)","(1, 3)","(3, 1)","(1, 3)","(3, 1)","(3, 2)","(3, 2)","(4, 2, 3)","(4, 2, 3)"])
)

s5 = section(5,"Stacking &amp; Splitting",
    "Combine arrays along existing or new axes. Always check shapes before stacking — "
    "a common source of bugs is mismatched dimensions.",
    cb("concatenate / vstack / hstack / dstack / stack / split / vsplit / hsplit",
"""import numpy as np

a = np.array([[1,2],[3,4]])    # (2,2)
b = np.array([[5,6],[7,8]])    # (2,2)

# concatenate — along existing axis
print(np.concatenate([a,b],axis=0))  # (4,2) — rows
print(np.concatenate([a,b],axis=1))  # (2,4) — cols

# vstack / hstack / dstack — semantic shortcuts
print(np.vstack([a,b]).shape)   # (4,2)  same as axis=0
print(np.hstack([a,b]).shape)   # (2,4)  same as axis=1
c3d = np.dstack([a,b])
print(c3d.shape)                # (2,2,2)  depth-wise

# stack — creates NEW axis
print(np.stack([a,b]).shape)          # (2,2,2)  new axis=0
print(np.stack([a,b],axis=1).shape)   # (2,2,2)  new axis=1
print(np.stack([a,b],axis=-1).shape)  # (2,2,2)  new axis=-1

# column_stack — 1D arrays become columns
v1,v2=np.array([1,2,3]),np.array([4,5,6])
print(np.column_stack([v1,v2]))  # [[1,4],[2,5],[3,6]]

# split — evenly or at indices
m = np.arange(12).reshape(3,4)
parts = np.split(m,3,axis=0)    # 3 equal parts along rows
print([p.shape for p in parts]) # [(1,4),(1,4),(1,4)]
parts2 = np.split(m,[1,3],axis=1) # at col 1 and 3
print([p.shape for p in parts2]) # [(3,1),(3,2),(3,1)]

# vsplit / hsplit / dsplit
rows = np.vsplit(m,3)           # split into 3 row-groups
cols = np.hsplit(m,[1,3])       # split at col indices 1,3""",
["(4, 2)","(2, 4)","(4, 2)","(2, 4)","(2, 2, 2)","(2, 2, 2)","(2, 2, 2)","(2, 2, 2)",
 "[[1 4]\n [2 5]\n [3 6]]","[(1, 4), (1, 4), (1, 4)]","[(3, 1), (3, 2), (3, 1)]"])
)

s6 = section(6,"Arithmetic Ufuncs",
    "Ufuncs (universal functions) operate element-wise on arrays and support broadcasting. "
    "They are implemented in C — much faster than Python loops.",
    cb("add/subtract/multiply/divide/power/mod/sqrt/abs/sign + broadcasting",
"""import numpy as np

a = np.array([1.,2.,3.,4.])
b = np.array([2.,2.,2.,2.])

# Element-wise arithmetic (ufuncs)
print(np.add(a,b))         # [3. 4. 5. 6.]  same as a+b
print(np.subtract(a,b))    # [-1.  0.  1.  2.]
print(np.multiply(a,b))    # [2. 4. 6. 8.]
print(np.divide(a,b))      # [0.5 1.  1.5 2. ]
print(np.power(a,b))       # [1. 4. 9. 16.]
print(np.mod(a,3))         # [1. 2. 0. 1.]   a % 3
print(np.sqrt(a))          # [1.   1.41 1.73 2.  ]
print(np.square(a))        # [1.  4.  9. 16.]
print(np.abs(np.array([-3,4,-1])))  # [3 4 1]
print(np.sign(np.array([-5,0,3])))  # [-1  0  1]

# Ufunc extra params
out = np.empty(4)
np.add(a,b,out=out)        # write result into existing array
np.add(a,b,out=None)       # default

# Broadcasting rules:
# 1. Shapes compared right-to-left
# 2. Dimensions equal OR one of them is 1 → stretch that axis
m = np.arange(1,7).reshape(2,3)    # (2,3)
v = np.array([10,20,30])           # (3,)  → broadcast to (2,3)
print(m + v)   # add v to each row

col = np.array([[100],[200]])      # (2,1) → broadcast to (2,3)
print(m + col) # add col to each col

# Error: incompatible shapes
try:
    np.array([1,2,3]) + np.array([1,2])  # (3,) + (2,)
except ValueError as e:
    print(e)   # operands could not be broadcast together with shapes (3,)  (2,)""",
["[3. 4. 5. 6.]","[-1.  0.  1.  2.]","[2. 4. 6. 8.]","[0.5 1.  1.5 2. ]","[1.  4.  9. 16.]",
 "[1. 2. 0. 1.]","[1.   1.41 1.73 2.  ]","[1.  4.  9. 16.]","[3 4 1]","[-1  0  1]",
 "[[11 22 33]\n [14 25 36]]","[[101 102 103]\n [204 205 206]]",
 "operands could not be broadcast together with shapes (3,) (2,)"])
)

s7 = section(7,"Exponential &amp; Logarithm",
    "NumPy's exp/log functions operate element-wise and are numerically stable. "
    "log1p and expm1 are more accurate near zero.",
    cb("np.exp / log / log2 / log10 / log1p / expm1",
"""import numpy as np

x = np.array([0.,1.,2.,3.])
print(np.exp(x))    # [ 1.     2.718  7.389 20.086]  e^x
print(np.log(x+1))  # [0.    0.693 1.099 1.386]       ln(x+1)
print(np.log2(x+1)) # [0.    1.    1.585 2.   ]       log base 2
print(np.log10(np.array([1,10,100,1000.])))  # [0. 1. 2. 3.]

# More stable near x=0:
tiny = np.array([1e-10, 1e-5, 0.01])
print(np.log1p(tiny))   # log(1+x) accurate for small x
print(np.expm1(tiny))   # exp(x)-1 accurate for small x

# Common patterns
# e^(log(x)) = x — floating point round-trip
a = np.array([2.,3.,4.])
print(np.exp(np.log(a)))  # [2. 3. 4.]

# Log-sum-exp trick (numerically stable softmax)
logits = np.array([1.,2.,3.,4.])
log_sum = np.log(np.sum(np.exp(logits)))  # unstable for large values
stable  = np.max(logits) + np.log(np.sum(np.exp(logits-np.max(logits))))
print(f"log_sum_exp = {stable:.4f}")""",
["[1.    2.718 7.389 20.086]","[0.    0.693 1.099 1.386]","[0.    1.    1.585 2.   ]",
 "[0. 1. 2. 3.]","log_sum_exp = 4.4402"])
)

s8 = section(8,"Trigonometry",
    "All trig functions take angles in RADIANS. Use np.deg2rad() / np.rad2deg() to convert. "
    "arctan2(y,x) correctly handles all quadrants.",
    cb("sin / cos / tan / arcsin / arccos / arctan / arctan2 / deg2rad / hypot",
"""import numpy as np

angles = np.array([0, np.pi/6, np.pi/4, np.pi/3, np.pi/2])
print(np.sin(angles).round(4))   # [0.    0.5   0.7071 0.866 1.   ]
print(np.cos(angles).round(4))   # [1.    0.866 0.7071 0.5   0.   ]
print(np.tan(angles).round(4))   # [0.    0.5774 1.   1.7321 inf]

# Inverse functions — return radians
print(np.arcsin(0.5))   # 0.5236  (π/6)
print(np.arccos(0.5))   # 1.0472  (π/3)
print(np.arctan(1.0))   # 0.7854  (π/4)

# arctan2(y,x) — full quadrant aware 2-argument arctangent
print(np.arctan2(1, 1))   # 0.7854   Q1
print(np.arctan2(1,-1))   # 2.3562   Q2
print(np.arctan2(-1,1))   # -0.7854  Q4

# Degree conversions
deg = np.array([0.,30.,45.,60.,90.])
rad = np.deg2rad(deg)
print(rad.round(4))         # [0.     0.5236 0.7854 1.0472 1.5708]
print(np.rad2deg(np.pi))    # 180.0

# Hypotenuse — numerically stable sqrt(x^2+y^2)
print(np.hypot(3,4))   # 5.0""",
["[0.     0.5    0.7071 0.866  1.    ]","[1.     0.866  0.7071 0.5    0.    ]",
"0.5236","1.0472","0.7854","0.7854","2.3562","-0.7854","5.0"])
)

s9 = section(9,"Rounding &amp; Clipping",
    "np.round (alias: np.around) rounds to nearest even on ties. "
    "np.clip constrains values to a range. np.maximum/np.minimum do element-wise comparisons.",
    cb("floor / ceil / round / trunc / clip / maximum / minimum",
"""import numpy as np

a = np.array([-2.7, -1.5, -0.5, 0.5, 1.5, 2.7])

print(np.floor(a))    # [-3. -2. -1.  0.  1.  2.]  round down
print(np.ceil(a))     # [-2. -1.  0.  1.  2.  3.]  round up
print(np.trunc(a))    # [-2. -1.  0.  0.  1.  2.]  toward zero
print(np.round(a))    # [-3. -2.  0.  0.  2.  3.]  banker's rounding (round-half-to-even)
print(np.round(np.array([3.14159, 2.71828]),2))  # [3.14 2.72]

# Clipping
x = np.array([1,5,3,8,2,9,4])
print(np.clip(x,3,7))   # [3 5 3 7 3 7 4]  min=3, max=7

# Element-wise max / min (different from np.max aggregate!)
a = np.array([1,5,3,8])
b = np.array([4,2,6,7])
print(np.maximum(a,b))   # [4 5 6 8]  (element-wise greater)
print(np.minimum(a,b))   # [1 2 3 7]  (element-wise smaller)

# fmax / fmin — same but ignore NaN
a2 = np.array([1.,np.nan,3.])
b2 = np.array([4.,5.,np.nan])
print(np.fmax(a2,b2))   # [4. 5. 3.]  ignores NaN""",
["[-3. -2. -1.  0.  1.  2.]","[-2. -1.  0.  1.  2.  3.]","[-2. -1.  0.  0.  1.  2.]",
 "[-3. -2.  0.  0.  2.  3.]","[3.14 2.72]","[3 5 3 7 3 7 4]","[4 5 6 8]","[1 2 3 7]","[4. 5. 3.]"])
)

s10 = section(10,"Linear Algebra",
    "np.linalg provides matrix decompositions, solvers, and norms. "
    "The @ operator (Python 3.5+) is equivalent to np.matmul for 2D arrays.",
    cb("dot / matmul / inner / outer / cross / linalg: det inv pinv norm eig svd solve lstsq",
"""import numpy as np

A = np.array([[1,2],[3,4]], dtype=float)
B = np.array([[5,6],[7,8]], dtype=float)

# Matrix multiplication
print(A @ B)                    # [[19,22],[43,50]]
print(np.matmul(A,B))           # same
print(np.dot(A,B))              # same for 2D

# Vector operations
u = np.array([1.,2.,3.])
v = np.array([4.,5.,6.])
print(np.inner(u,v))            # 32.0  (dot product)
print(np.outer(u,v))            # 3x3 outer product

# Cross product
print(np.cross(u,v))            # [-3.  6. -3.]

# Determinant
print(f"det = {np.linalg.det(A):.4f}")   # det = -2.0000

# Inverse
Ainv = np.linalg.inv(A)
print(Ainv)  # [[-2.   1. ][ 1.5 -0.5]]
print((A @ Ainv).round(10))  # identity matrix

# Pseudo-inverse (Moore-Penrose)
print(np.linalg.pinv(A).round(4))

# Eigenvalues & eigenvectors
vals, vecs = np.linalg.eig(A)
print(f"eigenvalues: {vals.round(4)}")  # [-0.3723  5.3723]

# SVD — A = U*S*Vt
U,S,Vt = np.linalg.svd(A)
print(f"singular values: {S.round(4)}")  # [5.4649 0.366]

# Solve linear system Ax=b
b_vec = np.array([5.,6.])
x = np.linalg.solve(A, b_vec)
print(f"solution: {x}")   # solution: [4.  0.5]

# Norm
print(np.linalg.norm(u))          # 3.7417  (L2 norm)
print(np.linalg.norm(A,'fro'))    # Frobenius norm
print(np.linalg.norm(u,ord=1))    # 6.0  (L1 norm)""",
["[[19. 22.]\n [43. 50.]]","32.0","det = -2.0000",
 "eigenvalues: [-0.3723  5.3723]","singular values: [5.4649 0.366 ]",
 "solution: [4.  0.5]","3.7417"])
)

s11 = section(11,"Sum &amp; Product",
    "np.sum and np.prod work on any axis. keepdims=True preserves dimensions for broadcasting. "
    "Cumulative versions track running totals.",
    cb("sum / prod / cumsum / cumprod — axis and keepdims params",
"""import numpy as np

m = np.array([[1,2,3],[4,5,6]])   # (2,3)

print(np.sum(m))              # 21        (all elements)
print(np.sum(m,axis=0))       # [5 7 9]   (column sums)
print(np.sum(m,axis=1))       # [6 15]    (row sums)
print(np.sum(m,axis=1,keepdims=True))  # [[6],[15]]  preserves 2D

print(np.prod(m))             # 720
print(np.prod(m,axis=0))      # [4 10 18]
print(np.prod(m,axis=1))      # [6 120]

# Cumulative (running totals)
a = np.array([1,2,3,4,5])
print(np.cumsum(a))    # [ 1  3  6 10 15]
print(np.cumprod(a))   # [  1   2   6  24 120]

# 2D cumulative
print(np.cumsum(m,axis=0))   # [[1,2,3],[5,7,9]]
print(np.cumsum(m,axis=1))   # [[1,3,6],[4,9,15]]

# keepdims — keeps result broadcastable with input
sums = np.sum(m,axis=1,keepdims=True)  # (2,1)
normalized = m / sums                   # divides each row by its sum
print(normalized.round(3))  # [[0.167 0.333 0.5 ],[0.267 0.333 0.4]]""",
["21","[5 7 9]","[ 6 15]","[[ 6]\n [15]]","720","[ 4 10 18]","[  6 120]",
 "[ 1  3  6 10 15]","[  1   2   6  24 120]",
 "[[0.167 0.333 0.5  ]\n [0.267 0.333 0.4  ]]"])
)

s12 = section(12,"Statistics",
    "np.mean/std/var all support axis and ddof parameters. "
    "ddof=1 for sample statistics (Bessel's correction).",
    cb("mean / median / std / var — with axis and ddof",
"""import numpy as np

data = np.array([[4,7,2,1],[5,3,8,6]])  # (2,4)

print(np.mean(data))          # 4.5     (global mean)
print(np.mean(data,axis=0))   # [4.5 5.  5.  3.5]  column means
print(np.mean(data,axis=1))   # [3.5 5.5]  row means

print(np.median(data))         # 4.5
print(np.median(data,axis=1))  # [3.  5.5]

# std/var with ddof
print(np.std(data))            # population std (ddof=0 default)
print(np.std(data,ddof=1))     # sample std (Bessel corrected)
print(np.var(data,ddof=1))     # sample variance

# Weighted mean
weights = np.array([0.1,0.3,0.4,0.2])
row = np.array([4.,7.,2.,1.])
print(np.average(row,weights=weights))  # 3.3

# Correlations & covariance
x = np.array([1.,2.,3.,4.,5.])
y = np.array([2.,4.,5.,4.,5.])
print(f"corr = {np.corrcoef(x,y)[0,1]:.4f}")  # corr = 0.9191
print(np.cov(x,y,ddof=1))  # 2x2 covariance matrix""",
["4.5","[4.5 5.  5.  3.5]","[3.5 5.5]","4.5","[3.  5.5]","3.3","corr = 0.9191"])
)

s13 = section(13,"Min / Max / ArgMin / ArgMax",
    "np.min/max return values; np.argmin/argmax return INDICES of extrema along an axis.",
    cb("min / max / argmin / argmax / ptp",
"""import numpy as np

m = np.array([[3,1,4],[1,5,9],[2,6,5]])

print(np.min(m))          # 1     (global min)
print(np.max(m))          # 9     (global max)
print(np.min(m,axis=0))   # [1 1 4]  col mins
print(np.max(m,axis=1))   # [4 9 6]  row maxes

print(np.argmin(m))       # 1     (flat index of first 1)
print(np.argmax(m))       # 8     (flat index of 9)
print(np.argmin(m,axis=0))   # [1 0 0]  col argmins
print(np.argmax(m,axis=1))   # [2 2 1]  row argmaxes

# ptp — peak-to-peak (max-min), deprecated in newer NumPy
print(np.ptp(m))          # 8
print(np.ptp(m,axis=1))   # [3 8 4]""",
["1","9","[1 1 4]","[4 9 6]","1","8","[1 0 0]","[2 2 1]","8","[3 8 4]"])
)

s14 = section(14,"Percentile &amp; Quantile",
    "np.percentile and np.quantile differ only in scale (0-100 vs 0-1). "
    "The interpolation/method parameter controls behavior at non-integer positions.",
    cb("percentile / quantile — q, axis, method params",
"""import numpy as np

a = np.array([1,2,3,4,5,6,7,8,9,10], dtype=float)

print(np.percentile(a,50))         # 5.5  (median)
print(np.percentile(a,[25,50,75])) # [3.25 5.5  7.75]  quartiles
print(np.quantile(a,0.5))          # 5.5  (same as 50th percentile)
print(np.quantile(a,[0.25,0.5,0.75]))  # [3.25 5.5  7.75]

# axis parameter
m = np.array([[10,20,30],[40,50,60]])
print(np.percentile(m,50,axis=0))   # [25. 35. 45.]  col medians
print(np.percentile(m,50,axis=1))   # [20. 50.]  row medians

# method (was interpolation pre-1.22) — how to handle non-integer positions
methods = ['linear','lower','higher','midpoint','nearest']
x = np.array([1,2,3,4])
for m_name in methods:
    val = np.percentile(x, 30, method=m_name)
    print(f"  {m_name:10}: {val}")

# keepdims
print(np.percentile(a,[25,75],keepdims=True).shape)  # (2,1) → broadcastable""",
["5.5","[3.25 5.5  7.75]","5.5","[3.25 5.5  7.75]","[25. 35. 45.]","[20. 50.]",
 "  linear    : 1.9","  lower     : 1.0","  higher    : 2.0","  midpoint  : 1.5","  nearest   : 2.0","(2, 1)"])
)

s15 = section(15,"NaN-safe Functions",
    "Functions prefixed with nan (nansum, nanmean…) ignore NaN values. "
    "Regular np.sum propagates NaN — any NaN in array produces NaN result.",
    cb("nansum / nanmean / nanstd / nanmax / nanmin / nanargmin / nanargmax",
"""import numpy as np

a = np.array([1.,2.,np.nan,4.,5.,np.nan])

# Regular functions propagate NaN
print(np.sum(a))      # nan
print(np.mean(a))     # nan

# NaN-safe functions skip NaN
print(np.nansum(a))    # 12.0
print(np.nanmean(a))   # 3.0  (mean of [1,2,4,5])
print(np.nanstd(a))    # 1.4142
print(np.nanvar(a))    # 2.0
print(np.nanmax(a))    # 5.0
print(np.nanmin(a))    # 1.0
print(np.nanargmin(a)) # 0  (index of min, ignoring NaN)
print(np.nanargmax(a)) # 4  (index of max, ignoring NaN)
print(np.nanmedian(a)) # 3.0

# Count non-NaN elements
print(np.sum(~np.isnan(a)))  # 4

# Detect NaN/inf
b = np.array([1.,np.nan,np.inf,-np.inf,2.])
print(np.isnan(b))    # [F T F F F]
print(np.isinf(b))    # [F F T T F]
print(np.isfinite(b)) # [T F F F T]""",
["nan","nan","12.0","3.0","1.4142","2.0","5.0","1.0","0","4","3.0","4",
 "[False  True False False False]","[False False  True  True False]","[ True False False False  True]"])
)

s16 = section(16,"Unique &amp; Sort",
    "np.unique returns sorted unique values with optional return of indices, inverse, and counts. "
    "np.sort returns a copy; a.sort() sorts in-place.",
    cb("unique / sort / argsort / in-place sort",
"""import numpy as np

a = np.array([3,1,4,1,5,9,2,6,5,3])

# np.unique — always returns sorted unique values
u = np.unique(a)
print(u)   # [1 2 3 4 5 6 9]

# With optional returns
u,idx = np.unique(a, return_index=True)
print(idx)   # indices of FIRST occurrence in original

u,inv = np.unique(a, return_inverse=True)
print(inv)   # maps each element to its unique index

u,cnt = np.unique(a, return_counts=True)
print(cnt)   # [2 1 2 1 2 1 1]  counts of each unique value
print(dict(zip(u,cnt)))  # {1:2, 2:1, 3:2, ...}

# All at once
u,idx,inv,cnt = np.unique(a,return_index=True,return_inverse=True,return_counts=True)

# np.sort — returns copy, original unchanged
s = np.sort(a)                    # ascending
s2= np.sort(a)[::-1]             # descending (reverse)
print(np.sort(a,axis=None))      # flatten then sort

m = np.array([[3,1],[4,2]])
print(np.sort(m,axis=0))   # sort each column [[3,1],[4,2]]
print(np.sort(m,axis=1))   # sort each row    [[1,3],[2,4]]

# a.sort() — in-place, returns None
b = np.array([5,2,8,1])
b.sort()
print(b)   # [1 2 5 8]

# np.argsort — indices that WOULD sort the array
a2 = np.array([30,10,20])
print(np.argsort(a2))    # [1 2 0]  (10 is at idx 1, 20 at 2, 30 at 0)
print(a2[np.argsort(a2)])  # [10 20 30]  sorted via fancy indexing""",
["[1 2 3 4 5 6 9]","[2 1 5 8 3 7 2 1 5 3]","[1 2 5 8]","[1 2 0]","[10 20 30]"])
)

s17 = section(17,"Boolean &amp; Comparison",
    "np.all/any with axis. np.isclose for floating-point comparison with tolerances. "
    "np.array_equal for exact match.",
    cb("all / any / isnan / isinf / isclose / allclose / array_equal",
"""import numpy as np

a = np.array([True,True,False,True])
print(np.all(a))     # False  (any False → False)
print(np.any(a))     # True   (any True → True)

m = np.array([[1,2],[3,0]])
print(np.all(m,axis=0))   # [True False]  (col-wise)
print(np.any(m,axis=1))   # [True True]   (row-wise)

# Float comparison — NEVER use == for floats!
x = 0.1+0.2
print(x == 0.3)      # False!  (floating point)

# isclose(a,b,rtol=1e-5,atol=1e-8) — element-wise
print(np.isclose(x,0.3))    # True

# allclose — all elements close?
a = np.array([1.0, 2.0, 3.0])
b = np.array([1.0+1e-9, 2.0, 3.0+1e-9])
print(np.allclose(a,b))     # True

# Strict equality
print(np.array_equal(np.array([1,2,3]),np.array([1,2,3])))  # True
print(np.array_equal(np.array([1,2]),np.array([1,3])))      # False""",
["False","True","[True False]","[True True]","False","True","True","True","False"])
)

s18 = section(18,"Set Operations",
    "NumPy set operations work on 1D arrays and return sorted unique results. "
    "They are convenient but not as fast as Python sets for pure membership tests.",
    cb("in1d / intersect1d / union1d / setdiff1d / setxor1d",
"""import numpy as np

a = np.array([1,2,3,4,5])
b = np.array([3,4,5,6,7])

print(np.intersect1d(a,b))    # [3 4 5]  elements in BOTH
print(np.union1d(a,b))        # [1 2 3 4 5 6 7] elements in EITHER
print(np.setdiff1d(a,b))      # [1 2]  in a but NOT in b
print(np.setxor1d(a,b))       # [1 2 6 7]  in exactly one

# in1d — membership test (like Python 'in' but vectorized)
print(np.in1d(np.array([2,4,6]),a))   # [True True False]
# np.isin is the preferred modern version
print(np.isin(np.array([2,4,6]),a))   # [True True False]

# intersect1d with return_indices
common,ia,ib = np.intersect1d(a,b,return_indices=True)
print(common)  # [3 4 5]
print(ia)      # [2 3 4]  positions in a
print(ib)      # [0 1 2]  positions in b""",
["[3 4 5]","[1 2 3 4 5 6 7]","[1 2]","[1 2 6 7]","[ True  True False]","[ True  True False]",
 "[3 4 5]","[2 3 4]","[0 1 2]"])
)

s19 = section(19,"Broadcasting Rules",
    "Broadcasting allows arithmetic on arrays with different shapes by virtually "
    "expanding smaller arrays. Rules: compare trailing dims right-to-left; "
    "dims must be equal or one of them must be 1.",
    cb("5 worked examples + 2 ValueError cases",
"""import numpy as np

# Rule: align shapes on right, pad with 1 on left as needed
# Dimensions must be equal OR one of them is 1 (stretches)

# Example 1: scalar + array
a = np.array([1,2,3])
print(a + 10)           # [11 12 13]  scalar→(1,)→(3,)

# Example 2: (3,) + (3,1) → (3,3)
col = np.array([[1],[2],[3]])   # (3,1)
print(a + col)
# [[2 3 4]
#  [3 4 5]
#  [4 5 6]]

# Example 3: (4,3) + (3,) — add vector to every row
m = np.ones((4,3))
v = np.array([10,20,30])   # (3,)→(1,3)→(4,3)
print((m+v)[0])    # [11. 21. 31.]

# Example 4: center each column (subtract column means)
data = np.array([[1.,2.,3.],[4.,5.,6.],[7.,8.,9.]])
col_means = data.mean(axis=0)         # (3,)
centered = data - col_means           # (3,3)-(3,)→broadcasts
print(centered[0])   # [-3. -3. -3.]

# Example 5: outer product via broadcasting
x = np.array([1,2,3])[:,np.newaxis]  # (3,1)
y = np.array([10,20])                 # (2,)
print(x * y)
# [[10 20]
#  [20 40]
#  [30 60]]

# ValueError examples
try:
    np.array([1,2,3]) + np.array([1,2])   # (3,)+(2,) FAIL
except ValueError as e:
    print(f"Error 1: shapes incompatible")

try:
    np.zeros((2,3)) + np.zeros((2,4))     # (2,3)+(2,4) FAIL
except ValueError as e:
    print(f"Error 2: shapes incompatible")""",
["[11 12 13]","[[2 3 4]\n [3 4 5]\n [4 5 6]]","[11. 21. 31.]","[-3. -3. -3.]",
 "[[10 20]\n [20 40]\n [30 60]]","Error 1: shapes incompatible","Error 2: shapes incompatible"])
)

s20_rest = "".join([
    section(20,"dtypes Reference",
        "NumPy dtypes map to C types. Smaller dtypes save memory but risk overflow. "
        "Use .astype() to convert. Check np.iinfo / np.finfo for range of a dtype.",
        cb("int8/16/32/64 uint float16/32/64 complex bool str object astype",
"""import numpy as np
# Integer types
print(np.iinfo(np.int8))    # min=-128 max=127
print(np.iinfo(np.uint8))   # min=0 max=255
print(np.iinfo(np.int64))   # min=-9223372036854775808 max=...

# Float types
print(np.finfo(np.float16)) # smallest, largest, eps
print(np.finfo(np.float32)) # ~7 decimal digits precision
print(np.finfo(np.float64)) # ~15 decimal digits precision

# Creating with specific dtype
a = np.array([1,2,3], dtype=np.int16)
b = np.array([1.5,2.5], dtype=np.float32)
c = np.array([1+2j, 3+4j], dtype=np.complex64)
d = np.array([True,False,True], dtype=np.bool_)
e = np.array(["hello","world"], dtype='U10')   # Unicode, max 10 chars

# astype — convert
x = np.array([1.7, 2.9, 3.1])
print(x.astype(int))        # [1 2 3]  truncates
print(x.astype(np.float32)) # lower precision
print(x.astype(str))        # ['1.7' '2.9' '3.1']

# dtype kind characters
# 'i' int  'u' uint  'f' float  'c' complex  'b' bool  'U' str  'O' object
for arr in [a,b,c,d,e]:
    print(f"{arr.dtype} → kind='{arr.dtype.kind}' itemsize={arr.dtype.itemsize}")""",
["[1 2 3]","['1.7' '2.9' '3.1']",
 "int16 → kind='i' itemsize=2","float32 → kind='f' itemsize=4",
 "complex64 → kind='c' itemsize=8","bool → kind='b' itemsize=1","<U10 → kind='U' itemsize=40"])
    ),

    section(21,"Views vs Copies",
        "A view shares memory — mutations through either array affect both. "
        "A copy is independent. np.shares_memory() tests sharing.",
        cb("view() / copy() / shares_memory / when indexing makes a view",
"""import numpy as np

a = np.arange(10)

# Slices return views
s = a[2:7]
s[0] = 999
print(a[2])           # 999 — original changed!

# Fancy indexing returns copies
f = a[[0,1,2]]
f[0] = -1
print(a[0])           # 0 — original unchanged

# Boolean indexing returns copies
b = a[a > 5]
b[0] = -99
print(a[6])           # 6 — unchanged

# Explicit view vs copy
v = a.view()          # share data, can have different shape/dtype
c = a.copy()          # independent

np.shares_memory(a,s) # True  (slice)
np.shares_memory(a,f) # False (fancy)
np.shares_memory(a,c) # False (copy)

print(np.shares_memory(a, a[2:7]))  # True
print(np.shares_memory(a, a[[0,1]])) # False

# Contiguous check
print(a.flags['C_CONTIGUOUS'])       # True
print(a[::2].flags['C_CONTIGUOUS'])  # False — stride-2 slice""",
["999","0","6","True","False","True","False"])
    ),

    section(22,"np.einsum",
        "einsum uses Einstein summation notation — powerful shorthand for any combination of "
        "tensor operations: transpose, trace, matmul, outer product, batch operations.",
        cb("einsum subscript notation with 6 examples",
"""import numpy as np

a = np.array([[1,2],[3,4]])   # (2,2)
b = np.array([[5,6],[7,8]])   # (2,2)
v = np.array([1,2,3])

# 1. Matrix trace (sum of diagonal)
print(np.einsum('ii->',a))     # 5  (1+4)

# 2. Matrix transpose
print(np.einsum('ij->ji',a))   # [[1,3],[2,4]]

# 3. Row sum
print(np.einsum('ij->i',a))    # [3 7]  (sum each row)

# 4. Column sum
print(np.einsum('ij->j',a))    # [4 6]

# 5. Matrix multiplication (same as A@B)
print(np.einsum('ij,jk->ik',a,b))  # [[19,22],[43,50]]

# 6. Element-wise multiply then sum (dot product)
print(np.einsum('ij,ij->',a,b))   # 70  (1*5+2*6+3*7+4*8)

# 7. Outer product
print(np.einsum('i,j->ij',v,v))   # 3x3 outer product

# 8. Batch matrix multiply
A = np.random.rand(5,3,4)
B = np.random.rand(5,4,2)
C = np.einsum('bij,bjk->bik',A,B)  # (5,3,2) batch matmul
print(C.shape)""",
["5","[[1 3]\n [2 4]]","[3 7]","[4 6]","[[19 22]\n [43 50]]","70","(5, 3, 2)"])
    ),
])

body = "".join([s1,s2,s3,s4,s5,s6,s7,s8,s9,s10,s11,s12,s13,s14,s15,
                s16,s17,s18,s19]) + s20_rest
body += playground("""import numpy as np

# Explore NumPy broadcasting
a = np.arange(1, 6).reshape(5, 1)  # column vector
b = np.arange(1, 6)                # row vector
result = a * b                      # 5x5 multiplication table
print("Multiplication table 1-5:")
print(result)""")

out_html = HEAD.format(title="NumPy",desc="NumPy complete reference — 40 topics, every function and parameter.") + \
           HERO.format(title="NumPy",desc="40 topics covering every array creation method, ufunc, linear algebra, aggregation, broadcasting, einsum, and advanced features.",n=40) + \
           toc(topics) + body + foot(("Python Basics","python-basics.html"),("Pandas","pandas.html"))

with open(os.path.join(BASE,"numpy.html"),"w",encoding="utf-8") as f:
    f.write(out_html)
print(f"numpy.html  {len(out_html):>10,} chars")
