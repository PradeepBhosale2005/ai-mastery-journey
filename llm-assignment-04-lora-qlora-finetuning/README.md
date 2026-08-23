# LLM Assignment 04: LoRA and QLoRA Fine-Tuning

This assignment compares LoRA and QLoRA fine-tuning for a 1B-scale LLaMA-style instruction model.

The default model is:

```text
TinyLlama/TinyLlama-1.1B-Chat-v1.0
```

## What it covers

- LoRA fine-tuning with frozen base model weights
- QLoRA fine-tuning with 4-bit `nf4` quantization through bitsandbytes
- Adapter target modules: `q_proj` and `v_proj`
- LoRA rank `r = 8`
- Learning rate `2e-4`
- Two training epochs by default
- Trainable parameter count
- Final training loss
- Peak GPU memory usage
- Three test prompts for qualitative response comparison

## Run in safe simulation mode

Simulation mode does not download a model and is useful for restricted laptops.

```powershell
cd C:\Users\pradeep.bhosale_jade\ai-mastery-journey
cd .\llm-assignment-04-lora-qlora-finetuning
python -m pip install -r requirements.txt
python lora_qlora_finetune.py
```

## Run real LoRA and QLoRA fine-tuning

Use this on Google Colab or a GPU machine with Hugging Face model download access.

```powershell
python lora_qlora_finetune.py --run-real --epochs 2
```

The script writes:

```text
results/lora_qlora_comparison_report.json
```

## Test

```powershell
python test_lora_qlora_config.py
```
