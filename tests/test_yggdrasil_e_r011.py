from yggdrasil.dispatch import dispatch


def test_r011_construct_atom():
    out = dispatch({"packet": "construct_atom"})
    assert out["rule"] == "R011"
    assert out["specialists"] == ["sigil.forge.construct"]
    assert out["result"] == "FOREIGN_SPECIALIST"
    assert out["home"] == "yggdrasil.viz"
    assert out["forecast_eligible"] is False
    assert out["frame"] is None


def test_r011_aliases():
    for packet in ("intent_glyph", "sigil_request"):
        out = dispatch({"packet": packet})
        assert out["rule"] == "R011"
        assert out["specialists"] == ["sigil.forge.construct"]


def test_r011b_tradition_chain():
    out = dispatch({"packet": "mixed_tradition_construct"})
    assert out["rule"] == "R011B"
    assert out["specialists"] == ["athanor.structure", "sigil.forge.construct"]
    assert out["result"] == "CHAIN"


def test_r011c_sign_chain():
    out = dispatch({"packet": "mixed_sign_construct"})
    assert out["rule"] == "R011C"
    assert out["specialists"] == ["semion.triad", "sigil.forge.construct"]
    assert out["result"] == "CHAIN"


def test_r011d_noctis_chain():
    out = dispatch({"packet": "noctis_sig"})
    assert out["rule"] == "R011D"
    assert out["specialists"] == ["noctis.interpret", "sigil.forge.construct"]
    assert out["result"] == "CHAIN"
    assert out["home"] == "yggdrasil.viz"


def test_forecast_still_wins():
    out = dispatch({"packet": "forecast_request", "intent": "forge a sigil"})
    assert out["rule"] == "R004"
    assert out["specialists"] == []


def test_viz_namespace_stays_topology():
    out = dispatch({"namespace": "yggdrasil.viz"})
    assert out["rule"] == "R009"
    assert out["specialists"] == ["yggdrasil.topology"]
    assert out["frame"]["route_class"] == "viz"
