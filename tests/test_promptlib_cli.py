from pathlib import Path

from zero_consult_clouds.config import Config, save_config


def _setup(tmp_path: Path) -> Path:
    cfg_path = tmp_path / "c.yaml"
    save_config(
        Config(
            api_key="k",
            model="m",
            model_tokenmax=16000,
            promptlib_dir=str(tmp_path / "pl"),
        ),
        cfg_path,
    )
    pl_dir = tmp_path / "pl"
    pl_dir.mkdir()
    (pl_dir / "1234promptlib-test.md").write_text("line1\nline2", encoding="utf-8")
    return cfg_path


def test_promptlib_cat(tmp_path, capsys):
    cfg = _setup(tmp_path)

    import importlib

    from zero_consult_clouds import cli as cli_mod

    importlib.reload(cli_mod)

    code = cli_mod.main(
        [
            "promptlib",
            "cat",
            "1234",
            "--config",
            str(cfg),
        ]
    )
    captured = capsys.readouterr()
    assert code == 0
    assert "line1" in captured.out


def test_promptlib_stats(tmp_path, capsys):
    cfg = _setup(tmp_path)

    import importlib

    from zero_consult_clouds import cli as cli_mod

    importlib.reload(cli_mod)

    code = cli_mod.main(
        [
            "promptlib",
            "stats",
            "--config",
            str(cfg),
        ]
    )
    captured = capsys.readouterr()
    assert code == 0
    assert "1 promptlib files" in captured.out


def test_promptlib_browse_passes_output(tmp_path, monkeypatch):
    cfg = _setup(tmp_path)
    out = tmp_path / "out.md"

    called = {}

    def fake_browse(path, filter_text="", output_file=None):
        called["path"] = path
        called["output_file"] = output_file
        return None

    monkeypatch.setattr("zero_consult_clouds.promptlib.browse", fake_browse)

    import importlib

    from zero_consult_clouds import cli as cli_mod

    importlib.reload(cli_mod)

    code = cli_mod.main(
        [
            "promptlib",
            "browse",
            "--config",
            str(cfg),
            "--output",
            str(out),
        ]
    )

    assert code == 0
    assert called["output_file"] == out


def test_browse_appends(tmp_path, monkeypatch):
    pl_dir = tmp_path / "pl"
    pl_dir.mkdir()
    p = pl_dir / "1234promptlib-test.md"
    p.write_text("line1", encoding="utf-8")

    out = tmp_path / "out.md"

    inputs = ["1", "y"]

    def fake_prompt(*args, **kwargs):
        return inputs.pop(0)

    monkeypatch.setattr("prompt_toolkit.PromptSession.prompt", fake_prompt)
    monkeypatch.setattr("builtins.input", lambda *a, **k: inputs.pop(0))

    from zero_consult_clouds import promptlib as pl

    pl.browse(pl_dir, output_file=out)

    assert out.read_text(encoding="utf-8").strip() == "line1"


def test_browse_fuzzy_match(tmp_path, monkeypatch):
    pl_dir = tmp_path / "pl"
    pl_dir.mkdir()
    p1 = pl_dir / "111promptlib-vibeunknown.md"
    p1.write_text("aaa", encoding="utf-8")
    (pl_dir / "222promptlib-other.md").write_text("bbb", encoding="utf-8")

    out = tmp_path / "out.md"

    inputs = ["vibe unknown", "y"]

    def fake_prompt(*args, **kwargs):
        return inputs.pop(0)

    monkeypatch.setattr("prompt_toolkit.PromptSession.prompt", fake_prompt)
    monkeypatch.setattr("builtins.input", lambda *a, **k: inputs.pop(0))

    from zero_consult_clouds import promptlib as pl

    selected = pl.browse(pl_dir, output_file=out)

    assert selected == p1
    assert out.read_text(encoding="utf-8").strip() == "aaa"
