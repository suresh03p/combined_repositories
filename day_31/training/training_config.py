"""Training configuration used for a small LoRA fine-tuning experiment."""

LEARNING_RATE = 2e-4
BATCH_SIZE = 4
GRADIENT_ACCUMULATION_STEPS = 8
NUM_EPOCHS = 3
WARMUP_RATIO = 0.1
WEIGHT_DECAY = 0.01
EVAL_STRATEGY = "epoch"
SAVE_STRATEGY = "epoch"
LOGGING_STEPS = 50
MAX_SEQ_LENGTH = 256

# Why these settings exist:
# - learning rate controls how quickly the model adapts
# - batch size affects stable gradient estimates and memory use
# - gradient accumulation simulates larger effective batches on limited hardware
# - epochs define how many times the model sees the data
# - warmup reduces early instability in optimization
# - weight decay regularizes the model and helps limit overfitting
# - evaluation and checkpoint frequency allow monitoring and restore points
