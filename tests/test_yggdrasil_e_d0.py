from yggdrasil.dispatch import dispatch


def test_r009_route_atom():
    out = dispatch({"namespace": "yggdrasil.ingest"})
    assert out["rule"] == "R009"
    assert out["specialists"] == ["yggdrasil.topology"]
    assert out["frame"]["route_class"] == "ingest"
    assert out["forecast_eligible"] is False


def test_r010_unknown_namespace():
    out = dispatch({"namespace": "yggdrasil.not_a_lane"})
    assert out["rule"] == "R010"
    assert out["result"] == "NOT_COMPUTABLE"
    assert out["failure"] == "UNKNOWN_NODE_GATE"


def test_r004_forecast_request():
    out = dispatch({"packet": "forecast_request"})
    assert out["rule"] == "R004"
    assert out["specialists"] == []
    assert out["result"] == "NOT_COMPUTABLE"


def test_r004_from_mapped_forecast_name():
    out = dispatch({"name": "pse_forecast"})
    assert out["rule"] == "R004"
    assert out["forecast_eligible"] is False


def test_foreign_slang_not_stolen():
    out = dispatch({"packet": "slang_atom"})
    assert out["rule"] == "R001"
    assert out["specialists"] == ["hyperlex.hyperlexical"]
    assert out["frame"] is None


def test_r004b_settled_not_scored_here():
    out = dispatch({"packet": "settled_forecast"})
    assert out["rule"] == "R004B"
    assert out["specialists"] == ["abx.brier"]
