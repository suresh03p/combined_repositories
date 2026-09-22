# Embedding Dimensions

An embedding is a vector: many numerical values produced by a trained model.

```text
Text
  |
Embedding model
  |
[0.12, 0.45, -0.32, ...]
  |
Many numerical values
```

A 3-dimensional vector has three coordinates. We can imagine it as a point in a room with length, width, and height. Ten dimensions have ten coordinates, although we cannot draw them easily. Real language models commonly produce 384, 768, or 1536 dimensions.

| Dimensions | Teaching picture |
| --- | --- |
| 3 | Easy to draw and visualize |
| 10 | More room for patterns |
| 100 | Many learned signals |
| 384 | `all-MiniLM-L6-v2` output in this project |
| 768 | Used by several larger language models |
| 1536 | Used by some commercial embedding APIs |

More dimensions do not automatically mean better search. Quality depends on the model, training data, domain, chunking, and evaluation. The vector is not simply a list of random numbers. During training, the model learns to arrange related language closer together in its embedding space. For example, `taxi` and `cab` may be closer than `taxi` and `salary`.

A vector database collection expects vectors of one consistent length. Do not mix a 384-dimensional vector with a 1536-dimensional vector in the same collection. If you change models, create a new collection and re-embed the documents.

The number itself is not a human-readable explanation of a sentence. Dimension 27 does not mean “vacation.” Meaning is distributed across many values, and we usually understand a vector by comparing it with other vectors rather than inspecting individual coordinates.
