# Quantization Comparison

## Overview
Quantization reduces the precision of model weights to save memory and improve inference efficiency. Depending on the model and hardware, the trade-off may include slight quality changes.

## Precision types
- FP32: highest precision, highest memory usage
- FP16: lower memory, usually faster on supported GPUs
- BF16: useful on modern accelerators with stable training/inference behavior
- INT8: memory savings and faster inference on supported hardware
- INT4: very compact but may reduce quality more noticeably

## Comparison dimensions
- Memory
- Latency
- Throughput
- Output quality

## Key rule
Lower precision is not automatically better. Choose the precision based on both hardware compatibility and output quality requirements.
