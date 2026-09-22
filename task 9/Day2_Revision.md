# Day 2 Revision - NumPy Concepts

## 20 Important Points

1. A NumPy array is a grid of values of the same data type.
2. Arrays can have one or more dimensions, called axes.
3. `shape` returns a tuple with the size of each dimension.
4. `ndim` gives the number of dimensions of the array.
5. `dtype` tells the data type stored in an array.
6. Indexing accesses one element by its position inside the array.
7. Slicing selects a range of elements using start:stop:step.
8. NumPy indexing supports negative indices and multi-dimensional indexing.
9. Broadcasting allows operations between arrays of different shapes.
10. `np.zeros()` creates an array filled with zeros.
11. `np.ones()` creates an array filled with ones.
12. `np.empty()` allocates an array without initializing values.
13. `np.full()` builds an array filled with a specified constant.
14. `np.eye()` generates a 2D identity matrix with ones on the diagonal.
15. `np.arange()` creates sequences of values with a fixed step.
16. `np.linspace()` creates evenly spaced values over a range.
17. `reshape()` changes the shape without changing data.
18. `flatten()` makes a copy of an array as 1D.
19. `ravel()` returns a view to flatten data when possible.
20. `transpose()` swaps axes and is useful for matrix operations.

## 10 Interview Questions with Answers

1. Q: What is a NumPy array?  
   A: A NumPy array is an N-dimensional grid of elements of the same type, optimized for numerical operations.

2. Q: How does `shape` differ from `ndim`?  
   A: `shape` returns the size of each axis as a tuple, while `ndim` returns the number of axes.

3. Q: What does broadcasting allow you to do?  
   A: Broadcasting allows arithmetic operations between arrays with compatible but different shapes by virtually expanding smaller arrays.

4. Q: How do you select the third row and second column from a 2D array?  
   A: Use `arr[2, 1]` assuming zero-based indexing.

5. Q: What is the difference between `flatten()` and `ravel()`?  
   A: `flatten()` returns a copy of the array as 1D, while `ravel()` returns a view when possible and is more memory efficient.

6. Q: When would you use `np.linspace()` instead of `np.arange()`?  
   A: Use `np.linspace()` when you want a fixed number of evenly spaced values, especially with non-integer steps.

7. Q: Explain `np.empty()`.  
   A: `np.empty()` allocates memory for a new array without initializing values, so the contents are arbitrary until you assign them.

8. Q: What is a boolean mask?  
   A: A boolean mask is an array of `True`/`False` values used to select elements from another array.

9. Q: How do you find unique values in a NumPy array?  
   A: Use `np.unique(array)` to return sorted unique values.

10. Q: Why are NumPy arrays preferred over Python lists for AI?  
    A: NumPy arrays are faster, use less memory, and support vectorized operations needed for large-scale numerical computation.

## 5 Doubts (if any)

1. When should I use `np.reshape()` versus `np.resize()`?  
2. Will `ravel()` always return a view, or can it return a copy sometimes?  
3. How does NumPy decide when array shapes are broadcast-compatible?  
4. Should I prefer `np.eye()` or `np.identity()` for identity matrices?  
5. What are the exact rules for slicing with negative step and reversed ranges?
