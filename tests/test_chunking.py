from zero_consult_clouds import chunking_processor as cp
from zero_consult_clouds.config import Config, save_config
from pathlib import Path
import types, sys

def test_chunking(tmp_path, monkeypatch):
    cfg_path = tmp_path / "c.yaml"
    save_config(Config(api_key="k", model="gpt-4o"), cfg_path)

    class DummyEnc:
        def encode(self, text):
            return list(text.split())

    def enc_for_model(model):
        return DummyEnc()

    monkeypatch.setitem(sys.modules, 'tiktoken', types.SimpleNamespace(encoding_for_model=enc_for_model))
    import zero_consult_clouds.helpers as helpers_mod
    helpers_mod.tiktoken = sys.modules['tiktoken']

    text = "word " * 500
    chunks = cp.chunk_content(text, config_path=cfg_path)
    assert chunks
    windows = cp.build_context_windows(chunks)
    assert len(windows) == len(chunks)
