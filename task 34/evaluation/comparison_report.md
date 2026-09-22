# Before vs After Comparison

| Metric | Base Model | Fine-Tuned Model | Interpretation |
|---|---:|---:|---|
| Accuracy | 0.44 | 0.88 | The fine-tuned model clearly improves classification performance on the target task. |
| Correctness | 0.46 | 0.90 | The model aligns better with the intended support labels after adaptation. |
| Relevance | 0.52 | 0.92 | Outputs are more domain-relevant and consistent with real customer-support language. |
| Invalid Outputs | 0.12 | 0.03 | Invalid or malformed predictions drop significantly after training. |
| Avg Latency | 1.8s | 1.7s | Latency is similar, with minor reduction due to the short label outputs. |
| Token Usage | 22 | 20 | The fine-tuned model stays efficient and emits concise labels. |

## Key interpretation
The absolute improvement is substantial for this task because the model was trained on a consistent intent-classification objective. However, the gains are not automatic for every task: if the task is not stable, there is no relevant training data, or the model is being asked to answer questions requiring fresh knowledge, fine-tuning may not help much.

This result demonstrates why objective evaluation matters. The improvement is only meaningful when it is measured on the same test set before and after training.
