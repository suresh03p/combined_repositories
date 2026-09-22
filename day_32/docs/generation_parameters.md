# Generation Parameters

## Overview
Generation parameters control how the model creates text. They affect creativity, determinism, output length, and variability.

## temperature
Lower values make output more deterministic and focused. Higher values increase randomness and creativity.

## top_k
This parameter limits sampling to the top K tokens at each step. Smaller values make output more constrained; larger values allow more variation.

## top_p
Named nucleus sampling, top_p chooses the smallest set of tokens whose cumulative probability exceeds a threshold. This can produce more natural and diverse outputs than pure top_k.

## max_new_tokens
This limits how many new tokens the model can generate. It directly influences output length.

## do_sample
When true, generation uses sampling instead of greedy decoding, enabling more diverse outputs. When false, decoding is more deterministic.

## Practical effects
- Creativity: increased by higher temperature and sampling
- Determinism: improved by lower temperature and do_sample=False
- Response length: controlled by max_new_tokens
- Output variability: influenced by temperature, top_k, top_p, and do_sample

## Example
A customer support model may prefer:
- temperature around 0.3-0.7
- top_p around 0.9
- max_new_tokens 64
- do_sample true for more natural replies

A strict classification or extraction workflow may prefer:
- temperature 0.0
- do_sample false
- short max_new_tokens
