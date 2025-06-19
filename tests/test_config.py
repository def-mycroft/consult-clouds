from pathlib import Path
from zero_consult_clouds import config


def test_setup_and_load(tmp_path):
    cfg_path = tmp_path / "c.yaml"
    cfg = config.setup_config(
        path=cfg_path,
        api_key="key",
        model="model",
        default_output_dir=str(tmp_path),
        promptlib_dir=str(tmp_path / "pl"),
        interactive=False,
    )
    loaded = config.load_config(cfg_path)
    assert cfg == loaded
    data = config.yaml.safe_load(cfg_path.read_text())
    assert data["api_key"] == "key"
    assert data["default_output_dir"] == str(tmp_path)
    assert data["promptlib_dir"] == str(tmp_path / "pl")
    assert "model-tokenmax" in data


