# Using Local LLMs on Apple Silicon

## Why Local LLMs?

Running LLMs locally on your M4 Mac Mini provides:
- **Complete privacy**: Data never leaves your machine
- **Zero API costs**: No per-token charges
- **Offline capability**: Works without internet
- **Full control**: Choose and customize models
- **Fast inference**: Apple Silicon optimization

## Recommended: Ollama

### Installation

```bash
# Install via Homebrew
brew install ollama

# Start Ollama service
ollama serve
```

### Download Models

```bash
# Recommended models for M4 Mac Mini

# Llama 3.2 (3B) - Fast, efficient
ollama pull llama3.2

# Llama 3.1 (8B) - Balanced performance
ollama pull llama3.1:8b

# Mistral (7B) - Good for code
ollama pull mistral

# Phi-3 (3.8B) - Microsoft, efficient
ollama pull phi3

# For embeddings
ollama pull nomic-embed-text
```

### Configure personAI

Update your `.env` file:

```bash
# Use Ollama instead of OpenAI
LLM_PROVIDER=ollama
OLLAMA_BASE_URL=http://localhost:11434
OLLAMA_MODEL=llama3.1:8b

# For embeddings
EMBEDDING_PROVIDER=ollama
EMBEDDING_MODEL=nomic-embed-text
```

### Test Ollama

```bash
# Test from command line
ollama run llama3.1:8b "What is data sovereignty?"

# Test via API
curl http://localhost:11434/api/generate -d '{
  "model": "llama3.1:8b",
  "prompt": "Explain personal AI assistants",
  "stream": false
}'
```

## Alternative: MLX

Apple's MLX framework optimized for Apple Silicon:

```bash
# Install MLX
pip install mlx mlx-lm

# Run models
python -m mlx_lm.generate \
  --model mlx-community/Llama-3.2-3B-Instruct-4bit \
  --prompt "What is sovereign AI?"
```

## Alternative: LM Studio

GUI application for running local LLMs:

1. Download from [lmstudio.ai](https://lmstudio.ai)
2. Install and launch
3. Download models from the UI
4. Start local server (OpenAI-compatible API)
5. Point personAI to LM Studio endpoint

## Performance Considerations

### M4 Mac Mini Specifications

- **M4 Chip**: 10-core CPU, up to 10-core GPU
- **Unified Memory**: 16GB base (upgradeable to 32GB)
- **Memory Bandwidth**: 100-120 GB/s

### Model Selection Guidelines

**16GB RAM**:
- 3B models: Excellent performance
- 7-8B models: Good performance
- 13B models: Possible with quantization
- 30B+ models: Not recommended

**32GB RAM**:
- 3-8B models: Excellent
- 13B models: Good performance
- 30-40B models: Possible with quantization

### Quantization

Use quantized models for better performance:

```bash
# 4-bit quantization (most efficient)
ollama pull llama3.1:8b-q4_0

# 8-bit quantization (better quality)
ollama pull llama3.1:8b-q8_0
```

## Integration with personAI

Update `main.py` to use Ollama:

```python
from langchain_community.llms import Ollama
from langchain_community.embeddings import OllamaEmbeddings

# Initialize Ollama LLM
llm = Ollama(
    model="llama3.1:8b",
    base_url="http://localhost:11434",
    temperature=0.7
)

# Initialize Ollama embeddings
embeddings = OllamaEmbeddings(
    model="nomic-embed-text",
    base_url="http://localhost:11434"
)
```

## Benchmarking

Test different models for your use case:

```bash
# Create benchmark script
cat > benchmark.py << 'EOF'
import time
from langchain_community.llms import Ollama

models = ["llama3.2", "llama3.1:8b", "mistral", "phi3"]
prompt = "Summarize this code: def hello(): print('world')"

for model in models:
    llm = Ollama(model=model)
    start = time.time()
    response = llm.invoke(prompt)
    elapsed = time.time() - start
    print(f"{model}: {elapsed:.2f}s - {len(response)} chars")
EOF

python benchmark.py
```

## Cost Comparison

### Cloud LLMs (Monthly estimate for moderate use)
- OpenAI GPT-4: ~$50-200/month
- OpenAI GPT-3.5: ~$10-50/month
- Anthropic Claude: ~$30-150/month

### Local LLMs (M4 Mac Mini)
- Electricity cost: ~$2-5/month
- No per-token charges
- **Annual savings**: $300-2000+

## Privacy Benefits

With local LLMs:
- ✅ No data sent to third parties
- ✅ HIPAA/GDPR compliant by default
- ✅ Process sensitive documents safely
- ✅ No rate limits or API outages
- ✅ Complete audit trail

## Troubleshooting

**Ollama not found**:
```bash
# Check installation
which ollama

# Restart service
pkill ollama && ollama serve
```

**Model too slow**:
- Use smaller model (3B instead of 8B)
- Try quantized versions (q4_0)
- Close other apps to free RAM
- Monitor: `sudo powermetrics --samplers cpu_power,gpu_power`

**Out of memory**:
```bash
# Check RAM usage
vm_stat

# Use smaller model or higher quantization
ollama pull llama3.2:3b-q4_0
```

## Next Steps

1. Install Ollama: `brew install ollama`
2. Download a model: `ollama pull llama3.1:8b`
3. Update personAI `.env` to use Ollama
4. Test with sample queries
5. Benchmark different models for your use case
