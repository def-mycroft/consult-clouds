from pathlib import Path
from zero_consult_clouds import config


def test_setup_and_load(tmp_path):
    cfg_path = tmp_path / "c.yaml"
    cfg = config.setup_config(
        path=cfg_path,
        api_key="key",
        default_model="model",
        interactive=False,
    )
    loaded = config.load_config(cfg_path)
    assert cfg == loaded
    data = config.yaml.safe_load(cfg_path.read_text())
    assert data["api_key"] == "key"


