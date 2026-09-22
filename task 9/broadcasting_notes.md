# Broadcasting Notes

## What is Broadcasting?

Broadcasting is NumPy's mechanism for applying arithmetic operations between arrays with different shapes. A smaller array is virtually expanded to match the larger array without making a full copy.

## 10 Observations

1. Broadcasting works when trailing dimensions are compatible.
2. A dimension of size 1 can be stretched to match the other array.
3. Scalars broadcast to any shape automatically.
4. Broadcasting avoids explicit Python loops for element-wise math.
5. The result shape is the maximum shape across input arrays.
6. Incompatible dimensions raise a `ValueError`.
7. Broadcasting can apply to 1D and 2D arrays, and higher dimensions.
8. It is used in both addition and multiplication operations.
9. Smaller array values are reused rather than copied physically.
10. Broadcasting can improve performance by reducing memory usage.

## 5 Advantages

1. Cleaner code: operations are expressed directly on arrays.
2. Faster execution than Python loops.
3. Less memory allocation than manually expanding arrays.
4. Works naturally with vectorized NumPy functions.
5. Enables convenient tensor math in machine learning workflows.

## 5 Real-life Use Cases

1. Adding a bias vector to every row of a feature matrix.
2. Scaling image pixel values by a single constant.
3. Applying a temperature adjustment across predictions.
4. Normalizing sensor data by subtracting the mean and dividing by standard deviation.
5. Computing pairwise distances by combining row and column vectors.
