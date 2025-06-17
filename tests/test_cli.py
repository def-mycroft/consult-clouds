from pathlib import Path
from zero_consult_clouds.config import Config, save_config


def test_convo(monkeypatch, tmp_path):
    cfg_path = tmp_path / "c.yaml"
    save_config(Config(api_key="k"), cfg_path)
    inp = tmp_path / "in.md"
    out = tmp_path / "out.md"
    inp.write_text("hello", encoding="utf-8")

    class Dummy:
        @staticmethod
        def create(**kwargs):
            return {"choices": [{"message": {"content": "hi"}}]}

    import types, sys
    openai_stub = types.SimpleNamespace(ChatCompletion=Dummy)
    monkeypatch.setitem(sys.modules, "openai", openai_stub)

    import importlib
    from zero_consult_clouds import cli as cli_mod
    importlib.reload(cli_mod)
    code = cli_mod.main([
        "convo",
        "-f",
        str(inp),
        "-o",
        str(out),
        "--config",
        str(cfg_path),
    ])
    assert code == 0
    assert out.read_text(encoding="utf-8") == "hi"




