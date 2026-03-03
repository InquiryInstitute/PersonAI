# Real-Time Fine-Tuning in personAI

## Overview

personAI now supports **real-time fine-tuning**, enabling your AI to continuously learn from interactions and truly "never forget" - inspired by OpenClaw's approach but with enhanced safety controls.

## What is Real-Time Fine-Tuning?

Unlike traditional RAG (Retrieval Augmented Generation) which only references external data, real-time fine-tuning actually **modifies the model's weights** during use, embedding new knowledge directly into the neural network.

### Benefits

- **True Learning**: Model internalizes patterns, not just references
- **Personalization**: Adapts to your communication style and preferences
- **Session Memory**: Remembers context across conversations
- **Privacy-First**: All training happens on-device (M4 Mac Mini) or in your cloud
- **No External Dependencies**: Doesn't require external vector stores once trained

## Architecture

```
User Query → personAI → Generate Response
     ↓                        ↓
Conversation Buffer ← Store Interaction
     ↓
[Every N interactions or manual trigger]
     ↓
Fine-Tuning Engine:
  1. Extract training pairs from buffer
  2. Content filter check (safety)
  3. Save checkpoint (for rollback)
  4. Perform backpropagation updates
  5. Save new checkpoint
  6. Log training metrics
```

## Setup

### 1. Enable Fine-Tuning

Edit your `.env` file:

```bash
# Enable fine-tuning
FINETUNING_ENABLED=true

# Auto fine-tune after interactions (or manual trigger only)
FINETUNING_AUTO=false

# Choose backend: ane (Apple Neural Engine), cpu, or cuda
FINETUNING_BACKEND=ane

# Training parameters
FINETUNING_LR=1e-5  # Learning rate
FINETUNING_STEPS=100  # Steps per session
FINETUNING_BUFFER_SIZE=100  # Recent messages to keep

# Safety controls
FINETUNING_REQUIRE_APPROVAL=true  # Require manual trigger
FINETUNING_CONTENT_FILTER=true  # Filter harmful content
FINETUNING_ROLLBACK=true  # Enable checkpoint rollback
```

### 2. Install Dependencies

```bash
pip install torch bitsandbytes peft
```

### 3. Initialize with Model

In your personAI setup:

```python
from finetuning import FineTuningEngine, FineTuningConfig

# Initialize engine
config = FineTuningConfig()
engine = FineTuningEngine(config)

# Initialize with your model
engine.initialize_model(model, tokenizer)
```

## Usage

### Manual Fine-Tuning

Trigger fine-tuning via API:

```bash
# Trigger a fine-tuning session
curl -X POST http://localhost:8080/finetune/trigger

# Trigger with custom step count
curl -X POST "http://localhost:8080/finetune/trigger?num_steps=500"
```

### Auto Fine-Tuning

Set `FINETUNING_AUTO=true` in `.env` to automatically fine-tune after every 10 interactions.

### Check Training Stats

```bash
curl http://localhost:8080/finetune/stats
```

Response:
```json
{
  "enabled": true,
  "stats": {
    "total_steps": 1000,
    "sessions": 10,
    "avg_steps_per_second": 107.5,
    "avg_loss": 0.342
  }
}
```

### Review Buffer

See what conversations are queued for training:

```bash
curl http://localhost:8080/finetune/buffer
```

### Rollback

If fine-tuning produces unwanted results:

```bash
# Rollback to latest checkpoint
curl -X POST http://localhost:8080/finetune/rollback

# Rollback to specific checkpoint
curl -X POST "http://localhost:8080/finetune/rollback?checkpoint_name=pre_finetune"
```

## Performance Targets

### M4 Mac Mini (Apple Neural Engine)
- **Target**: 107 steps/second (from OpenClaw benchmarks)
- **ANE Utilization**: ~11% for production workloads
- **Power**: Silent, low-power operation
- **Memory**: 16GB handles 3-8B models, 32GB for 13B+

### Cloud (CPU/CUDA)
- **CPU**: 10-30 steps/second
- **CUDA (GPU)**: 50-200 steps/second depending on GPU
- **Cost**: Negligible for parameter-efficient fine-tuning

## Safety Controls

### 1. Content Filtering

Automatically filters unsafe content before training:
- Hate speech
- Violence
- Explicit content
- Harmful instructions

Configure in `.env`:
```bash
FINETUNING_CONTENT_FILTER=true
```

### 2. Approval Required

Require manual approval before any fine-tuning:
```bash
FINETUNING_REQUIRE_APPROVAL=true
```

### 3. Checkpoint Rollback

Every fine-tuning session automatically saves checkpoints:
- Pre-training checkpoint
- Post-training checkpoint
- Maintains last N checkpoints (configurable)

Rollback instantly if needed.

### 4. Audit Logging

All fine-tuning sessions are logged:
- Timestamp
- Number of steps
- Training loss
- Steps per second
- Number of training pairs used

Export logs:
```python
engine.export_training_log("training_history.json")
```

## Parameter-Efficient Fine-Tuning (LoRA)

For efficiency, personAI fine-tunes only selected layers:
- Last 2 transformer blocks by default
- Reduces training time and memory
- Maintains base model performance

You can customize in `finetuning/engine.py`:
```python
def _select_trainable_parameters(self):
    # Fine-tune only last N layers
    layers = self.model.transformer.h[-2:]  # Adjust N here
```

## Advanced: Apple Neural Engine

### ANE Architecture

The Apple Neural Engine accelerates:
- Matrix operations (attention, feed-forward)
- Quantized operations (4-bit, 8-bit)
- Low-precision training

### Accessing ANE

Current implementation uses Metal Performance Shaders (MPS):
```python
device = "mps" if torch.backends.mps.is_available() else "cpu"
```

For direct ANE access (requires private APIs):
- See OpenClaw's implementation
- Use `ane_transformers` library (experimental)
- Requires macOS developer access

### Optimization Tips

1. **Use quantized models**: 4-bit or 8-bit
2. **Batch size = 1**: Optimal for ANE
3. **Sequence length ≤ 512**: Balance speed/context
4. **FP16 precision**: Native to ANE

## Comparison: Fine-Tuning vs RAG

| Feature | RAG | Real-Time Fine-Tuning |
|---------|-----|----------------------|
| Speed | Fast (retrieval) | Slower (training) |
| Memory | Requires vector DB | Embedded in model |
| Personalization | Limited | Deep |
| Persistence | External storage | Model weights |
| Setup | Simple | Moderate |
| Privacy | Depends on vector DB | Fully on-device |

**Best approach**: Use both! RAG for quick facts, fine-tuning for style and patterns.

## Troubleshooting

### "Fine-tuning disabled"
Check `.env`: `FINETUNING_ENABLED=true`

### "Model not initialized"
Call `engine.initialize_model(model, tokenizer)` after loading model

### Slow training
- Reduce `FINETUNING_STEPS`
- Use smaller model (3B vs 8B)
- Check `FINETUNING_BACKEND` (ane vs cpu)

### High memory usage
- Reduce `FINETUNING_BUFFER_SIZE`
- Use gradient checkpointing
- Fine-tune fewer layers

### Content filtered out
- Review buffer: `GET /finetune/buffer`
- Adjust content filter if too aggressive
- Check training pairs for patterns

## Future Enhancements

- [ ] Direct ANE API integration (waiting on Apple)
- [ ] Multi-layer LoRA adapters
- [ ] Distributed fine-tuning across devices
- [ ] Continual learning strategies (prevent catastrophic forgetting)
- [ ] Fine-tuning analytics dashboard
- [ ] Model merging (combine multiple fine-tuned versions)

## References

- OpenClaw real-time fine-tuning: [X post](https://x.com/brianroemmele/status/2028524908779802736)
- Apple Neural Engine: [Apple ML Compute](https://developer.apple.com/ml-compute/)
- LoRA: [Parameter-Efficient Fine-Tuning](https://arxiv.org/abs/2106.09685)
- PyTorch MPS: [Metal Backend](https://pytorch.org/docs/stable/notes/mps.html)
