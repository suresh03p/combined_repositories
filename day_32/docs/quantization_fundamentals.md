# Quantization Fundamentals

Quantization changes the numeric precision used to store and process model parameters.

- FP32: highest precision, highest memory use, slowest bandwidth footprint
- FP16: common mixed-precision format on GPUs, lower memory with good quality
- BF16: good support on newer hardware and often stable for inference
- INT8: smaller memory profile, can improve throughput, but quality must be checked
- INT4: very compact but more likely to affect output quality

## Relationship
Precision affects memory usage, inference speed, and output quality. Lower precision often reduces memory and may increase speed, but can also cause quality changes or compatibility issues depending on the model and hardware.

## Production takeaway
Do not assume lower precision is always better. The best choice depends on the target hardware, latency budget, throughput goals, and acceptance criteria for output quality.
