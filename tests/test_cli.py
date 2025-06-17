from pathlib import Path
from zero_consult_clouds.config import Config, save_config


def test_convo(monkeypatch, tmp_path):
    cfg_path = tmp_path / "c.yaml"
    save_config(
        Config(api_key="k", default_output_dir=str(tmp_path)),
        cfg_path,
    )
    inp = tmp_path / "in.md"
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
        "--config",
        str(cfg_path),
    ])
    assert code == 0
    out = tmp_path / "output.md"
    assert out.read_text(encoding="utf-8") == "hi"
    hist = tmp_path / "history.md"
    assert hist.exists()


def test_dev_update_toc(tmp_path):
    docs_dir = tmp_path / "docs"
    docs_dir.mkdir()
    (docs_dir / "a.md").write_text("# Title", encoding="utf-8")

    import importlib
    from zero_consult_clouds import cli as cli_mod
    importlib.reload(cli_mod)
    code = cli_mod.main([
        "dev",
        "--update-toc",
        "--docs-dir",
        str(docs_dir),
    ])
    assert code == 0
    contents = docs_dir / "CONTENTS.md"
    assert contents.exists()


def test_dev_new_doc(tmp_path):
    docs_dir = tmp_path / "docs"

    import importlib
    from zero_consult_clouds import cli as cli_mod
    importlib.reload(cli_mod)
    code = cli_mod.main([
        "dev",
        "--new-doc",
        "--docs-dir",
        str(docs_dir),
    ])
    assert code == 0
    files = list(docs_dir.glob("*.md"))
    assert len(files) == 1
    assert files[0].read_text(encoding="utf-8").startswith("# unnamed")




