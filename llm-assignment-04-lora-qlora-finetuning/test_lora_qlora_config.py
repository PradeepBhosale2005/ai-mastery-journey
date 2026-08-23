from lora_qlora_finetune import TEST_PROMPTS, create_lora_config, simulate_comparison


def test_lora_config_targets_attention_layers():
    config = create_lora_config()
    assert config.r == 8
    assert set(config.target_modules) == {"q_proj", "v_proj"}


def test_simulation_report_contains_lora_and_qlora():
    report = simulate_comparison()
    assert "lora" in report
    assert "qlora" in report
    assert report["lora"]["trainable_parameters"]["percent"] > 0
    assert report["qlora"]["peak_gpu_memory_mb"] < report["lora"]["peak_gpu_memory_mb"]


def test_three_test_prompts_are_present():
    assert len(TEST_PROMPTS) == 3
