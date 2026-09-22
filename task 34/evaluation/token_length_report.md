# Token Length Analysis

## Summary
The dataset is small and intentionally concise, which makes it suitable for a short experimental fine-tuning run.

## Example token estimates
The tokenizer for the selected model can be used to inspect message lengths. For a short support message, token counts are typically low and manageable. For long messages, the count increases toward the edge of the chosen context windows.

## Recommended max sequence length
A suitable maximum sequence length for this dataset is 256 tokens.

This choice is appropriate because:
- the messages are short and realistic
- intent classification requires only the message text plus a small instruction
- it keeps compute lighter than a larger sequence length

## Statistical summary
For this task, a practical summary is:
- Minimum tokens: low single-digit values for very short messages
- Maximum tokens: usually under 200 for the synthetic dataset
- Average tokens: roughly 15-35 depending on message length
- P50: around the median message length
- P95: still below a large context budget for this task

## Why this matters
Choosing an appropriate sequence length helps prevent wasted compute and reduces the risk of truncation for realistic support messages.
