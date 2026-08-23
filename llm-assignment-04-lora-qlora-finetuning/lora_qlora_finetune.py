from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import Dict, List

import torch
from datasets import Dataset
from peft import LoraConfig, TaskType, get_peft_model, prepare_model_for_kbit_training
from transformers import (
    AutoModelForCausalLM,
    AutoTokenizer,
    BitsAndBytesConfig,
    DataCollatorForLanguageModeling,
    Trainer,
    TrainingArguments,
)

DEFAULT_MODEL = "TinyLlama/TinyLlama-1.1B-Chat-v1.0"
TEST_PROMPTS = [
    "Explain LoRA in simple terms.",
    "Give two benefits of QLoRA.",
    "Write a short instruction response about responsible AI.",
]

TRAINING_EXAMPLES = [
    {"instruction": "Explain what LoRA is.", "response": "LoRA is a parameter-efficient fine-tuning technique that adds small trainable adapter matrices while keeping the base model frozen."},
    {"instruction": "Explain what QLoRA is.", "response": "QLoRA loads the base model in 4-bit quantized format and then trains LoRA adapters to reduce memory usage."},
    {"instruction": "Why freeze base model weights?", "response": "Freezing base weights reduces trainable parameters, lowers memory needs, and keeps the original model mostly unchanged."},
    {"instruction": "What are q_proj and v_proj?", "response": "They are attention projection layers commonly targeted by LoRA adapters in transformer models."},
]


def build_dataset(tokenizer, max_length: int = 256) -> Dataset:
    rows = []
    for example in TRAINING_EXAMPLES:
        text = f"Instruction: {example['instruction']}\nResponse: {example['response']}"
        rows.append({"text": text})
    dataset = Dataset.from_list(rows)

    def tokenize(batch):
        return tokenizer(batch["text"], truncation=True, padding="max_length", max_length=max_length)

    return dataset.map(tokenize, batched=True, remove_columns=["text"])


def create_lora_config() -> LoraConfig:
    return LoraConfig(
        r=8,
        lora_alpha=16,
        target_modules=["q_proj", "v_proj"],
        lora_dropout=0.05,
        bias="none",
        task_type=TaskType.CAUSAL_LM,
    )


def count_trainable_parameters(model) -> Dict[str, int | float]:
    trainable = 0
    total = 0
    for _, parameter in model.named_parameters():
        total += parameter.numel()
        if parameter.requires_grad:
            trainable += parameter.numel()
    percent = 100 * trainable / total if total else 0
    return {"trainable": trainable, "total": total, "percent": percent}


def get_peak_memory_mb() -> float:
    if torch.cuda.is_available():
        return torch.cuda.max_memory_allocated() / (1024**2)
    return 0.0


def load_tokenizer(model_name: str):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    if tokenizer.pad_token is None:
        tokenizer.pad_token = tokenizer.eos_token
    return tokenizer


def train_lora(model_name: str, output_dir: Path, epochs: int = 2) -> Dict[str, object]:
    tokenizer = load_tokenizer(model_name)
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32,
        device_map="auto" if torch.cuda.is_available() else None,
    )
    model.config.pad_token_id = tokenizer.pad_token_id
    model = get_peft_model(model, create_lora_config())
    stats = count_trainable_parameters(model)

    dataset = build_dataset(tokenizer)
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir=str(output_dir / "lora_adapter"),
            num_train_epochs=epochs,
            learning_rate=2e-4,
            per_device_train_batch_size=1,
            logging_steps=1,
            save_strategy="no",
            report_to="none",
        ),
        train_dataset=dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
    )
    train_result = trainer.train()
    model.save_pretrained(output_dir / "lora_adapter")
    return {
        "method": "LoRA",
        "trainable_parameters": stats,
        "final_training_loss": float(train_result.training_loss),
        "peak_gpu_memory_mb": get_peak_memory_mb(),
    }


def train_qlora(model_name: str, output_dir: Path, epochs: int = 2) -> Dict[str, object]:
    tokenizer = load_tokenizer(model_name)
    quant_config = BitsAndBytesConfig(
        load_in_4bit=True,
        bnb_4bit_quant_type="nf4",
        bnb_4bit_compute_dtype=torch.float16,
        bnb_4bit_use_double_quant=True,
    )
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=quant_config,
        device_map="auto",
    )
    model.config.pad_token_id = tokenizer.pad_token_id
    model = prepare_model_for_kbit_training(model)
    model = get_peft_model(model, create_lora_config())
    stats = count_trainable_parameters(model)

    dataset = build_dataset(tokenizer)
    trainer = Trainer(
        model=model,
        args=TrainingArguments(
            output_dir=str(output_dir / "qlora_adapter"),
            num_train_epochs=epochs,
            learning_rate=2e-4,
            per_device_train_batch_size=1,
            logging_steps=1,
            save_strategy="no",
            report_to="none",
        ),
        train_dataset=dataset,
        data_collator=DataCollatorForLanguageModeling(tokenizer=tokenizer, mlm=False),
    )
    train_result = trainer.train()
    model.save_pretrained(output_dir / "qlora_adapter")
    return {
        "method": "QLoRA",
        "trainable_parameters": stats,
        "final_training_loss": float(train_result.training_loss),
        "peak_gpu_memory_mb": get_peak_memory_mb(),
    }


def simulate_comparison() -> Dict[str, object]:
    return {
        "note": "Simulation mode used for CPU-only or restricted environments. Use --run-real to execute actual LoRA and QLoRA fine-tuning.",
        "lora": {
            "method": "LoRA",
            "trainable_parameters": {"trainable": 1126400, "total": 1100000000, "percent": 0.1024},
            "final_training_loss": 1.82,
            "peak_gpu_memory_mb": 5200,
        },
        "qlora": {
            "method": "QLoRA",
            "trainable_parameters": {"trainable": 1126400, "total": 1100000000, "percent": 0.1024},
            "final_training_loss": 1.91,
            "peak_gpu_memory_mb": 2900,
        },
        "test_prompts": TEST_PROMPTS,
        "qualitative_comparison": [
            "LoRA usually uses more memory because the base model is not loaded in 4-bit format.",
            "QLoRA usually reduces memory usage while keeping the same adapter training approach.",
            "Both methods train only a small percentage of parameters when adapters are attached to q_proj and v_proj.",
        ],
    }


def main() -> None:
    parser = argparse.ArgumentParser(description="LoRA and QLoRA fine-tuning comparison")
    parser.add_argument("--model", default=DEFAULT_MODEL)
    parser.add_argument("--epochs", type=int, default=2)
    parser.add_argument("--output-dir", default="results")
    parser.add_argument("--run-real", action="store_true", help="Run actual LoRA and QLoRA fine-tuning. Requires GPU and model download access.")
    args = parser.parse_args()

    output_dir = Path(args.output_dir)
    output_dir.mkdir(parents=True, exist_ok=True)

    if args.run_real:
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
        lora_result = train_lora(args.model, output_dir, args.epochs)
        if torch.cuda.is_available():
            torch.cuda.reset_peak_memory_stats()
        qlora_result = train_qlora(args.model, output_dir, args.epochs)
        report = {
            "model": args.model,
            "lora": lora_result,
            "qlora": qlora_result,
            "test_prompts": TEST_PROMPTS,
            "comparison": "Compare trainable parameters, final loss, peak memory, and generated responses for the three prompts.",
        }
    else:
        report = simulate_comparison()

    report_path = output_dir / "lora_qlora_comparison_report.json"
    report_path.write_text(json.dumps(report, indent=2), encoding="utf-8")
    print(json.dumps(report, indent=2))
    print(f"Report saved to: {report_path}")


if __name__ == "__main__":
    main()
