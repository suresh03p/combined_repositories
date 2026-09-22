"""LoRA configuration for a small customer support intent classifier."""

LORA_RANK = 8
LORA_ALPHA = 16
LORA_DROPOUT = 0.05
TARGET_MODULES = ["q", "v"]

# Why these settings exist:
# - rank controls the dimensionality of the trainable adapter space
# - alpha scales the LoRA update magnitude
# - dropout reduces overfitting on small datasets
# - target modules focus adaptation on the transformer attention weights
