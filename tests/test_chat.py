from zero_consult_clouds.config import Config, save_config


def test_send(monkeypatch, tmp_path):
    cfg_path = tmp_path / "c.yaml"
    save_config(Config(api_key="k", default_model="m"), cfg_path)

    result = {"choices": [{"message": {"content": "hi"}}]}

    class Dummy:
        @staticmethod
        def create(**kwargs):
            return result

    import types, sys
    openai_stub = types.SimpleNamespace(ChatCompletion=Dummy)
    monkeypatch.setitem(sys.modules, "openai", openai_stub)

    import importlib
    from zero_consult_clouds import chat as chat_mod
    importlib.reload(chat_mod)
    ChatGPT = chat_mod.ChatGPT

    chat = ChatGPT(config_path=cfg_path)
    reply = chat.send("hello")
    assert reply == "hi"
    assert chat.history[0]["content"] == "hello"
    assert chat.last_response == result


