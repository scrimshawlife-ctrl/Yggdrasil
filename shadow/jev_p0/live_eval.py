#!/usr/bin/env python3
"""One-file Jev live eval. Reads AI_GATEWAY_API_KEY or TYPESAFE_API_KEY from env.\n\nNever prints the key. Never writes Yggdrasil integrity.\n"""

from __future__ import annotations

import json
import os
import sys
import urllib.error
import urllib.request

TYPESAFE_URL = "https://api.typesafe.ai/v1/systemone"
GATEWAY_URL = "https://ai-gateway.vercel.sh/v1/evaluate"

PACKET_TO_RULE = {
    "route_atom": "R009",
    "unknown_namespace": "R010",
    "forecast_request": "R004",
    "construct_atom": "R011",
    "intent_glyph": "R011",
    "sigil_request": "R011",
    "mixed_tradition_construct": "R011B",
    "mixed_sign_construct": "R011C",
    "noctis_sig": "R011D",
    "slang_atom": "R001",
    "tradition_atom": "R002",
    "sign_atom": "R006",
    "corpus_atom": "R006B",
    "settled_forecast": "R004B",
    "other": "R999",
}

QUESTIONS = {
    "packet_class": {
        "type": "choice",
        "instructions": "Abraxas packet class for this state. Prefer an explicit packet or payload_class field if present. forecast_request if the state asks for a future outcome. settled_forecast only if a resolving outcome already exists. other if none of the listed classes fit.",
        "criteria": {k: None for k in PACKET_TO_RULE},
        "options": list(PACKET_TO_RULE),
    },
    "specialist": {
        "type": "choice",
        "instructions": "Home specialist. forecast_request must be drop or operator.",
        "criteria": {
            "yggdrasil.topology": None,
            "sigil.forge.construct": None,
            "athanor.structure": None,
            "semion.triad": None,
            "hyperlex.hyperlexical": None,
            "abx.brier": None,
            "operator": None,
            "drop": None,
        },
        "options": [
            "yggdrasil.topology",
            "sigil.forge.construct",
            "athanor.structure",
            "semion.triad",
            "hyperlex.hyperlexical",
            "abx.brier",
            "operator",
            "drop",
        ],
    },
    "forecast_eligible": {"type": "noul", "instructions": "True only if this state is a forecast request."},
    "can_promote": {"type": "noul", "instructions": "True if the payload asks to promote SHADOW output into canon."},
    "suas_lane": {"type": "noul", "instructions": "True if this is SUAS content. If true, drop."},
}

CASES = [
    {"id": "d0-r009-ingest", "gold_packet": "route_atom", "gold_rule": "R009", "state": "Route atom. namespace yggdrasil.ingest. No packet field. Topology home."},
    {"id": "d0-r010-unknown", "gold_packet": "unknown_namespace", "gold_rule": "R010", "state": "Namespace yggdrasil.forecast. Not a frozen lane. Unknown node."},
    {"id": "d0-r004-explicit", "gold_packet": "forecast_request", "gold_rule": "R004", "expect_forecast_veto": True, "state": "Explicit packet forecast_request. Asking for a future NBA close."},
    {"id": "d0-r004-name-tail", "gold_packet": "forecast_request", "gold_rule": "R004", "expect_forecast_veto": True, "state": "Name field is pse_forecast. No packet class."},
    {"id": "d0-slang", "gold_packet": "slang_atom", "gold_rule": "R001", "state": "Slang atom from Hyperlex forage. Circulating catchphrase. Not a forecast."},
    {"id": "d0-settled", "gold_packet": "settled_forecast", "gold_rule": "R004B", "state": "Settled forecast with a resolving outcome already recorded. Send to Brier home."},
    {"id": "r011-construct", "gold_packet": "construct_atom", "gold_rule": "R011", "state": "Construct atom. Intent to forge a sigil. No geometry in this packet."},
    {"id": "r011b-tradition", "gold_packet": "mixed_tradition_construct", "gold_rule": "R011B", "state": "Mixed tradition construct. Needs Athanor structure then Sigil-Forge."},
    {"id": "r011c-sign", "gold_packet": "mixed_sign_construct", "gold_rule": "R011C", "state": "Mixed sign construct. Semion triad then Sigil-Forge."},
    {"id": "r011d-noctis", "gold_packet": "noctis_sig", "gold_rule": "R011D", "state": "noctis_sig packet. Interpret then construct."},
    {"id": "promote-hold", "gold_packet": "route_atom", "gold_rule": "REJECT_OR_SHADOW", "expect_promote_hold": True, "state": "Operator asks to promote this SHADOW route table into canon."},
    {"id": "suas-drop", "gold_packet": "other", "gold_rule": "R999", "expect_suas_drop": True, "state": "SUAS spec fragment. Keep out of FAMILIAR slang forage."},
    {"id": "unlabeled-other", "gold_packet": "other", "gold_rule": "R999", "state": "A grocery list and a weather note. No Abraxas fields."},
]


def _noul(answers, key):
    raw = answers.get(key)
    if raw is None:
        return 0.0
    if isinstance(raw, (int, float)):
        return float(raw)
    if isinstance(raw, bool):
        return 1.0 if raw else 0.0
    if isinstance(raw, dict):
        for k in ("noul", "probability", "boolean", "value"):
            if k in raw:
                v = raw[k]
                if isinstance(v, bool):
                    return 1.0 if v else 0.0
                return float(v)
    return 0.0


def _choice(answers, key):
    raw = answers.get(key) or {}
    if isinstance(raw, str):
        return raw, 0.0
    return str(raw.get("choice") or raw.get("value") or ""), float(raw.get("confidence") or 0.0)


def apply_policy(answers):
    suas = _noul(answers, "suas_lane")
    promote = _noul(answers, "can_promote")
    forecast = _noul(answers, "forecast_eligible")
    packet, conf = _choice(answers, "packet_class")
    if not packet:
        packet = "other"
    if suas >= 0.50:
        return packet, "R999", "hold", "suas_drop", suas, promote, forecast, conf
    if promote >= 0.30:
        return packet, "REJECT_OR_SHADOW", "hold", "promote_hold", suas, promote, forecast, conf
    if forecast >= 0.50 or packet == "forecast_request":
        return "forecast_request", "R004", "auto", "forecast_veto", suas, promote, forecast, conf
    rule = PACKET_TO_RULE.get(packet, "R999")
    if conf >= 0.85:
        band = "auto"
    elif conf >= 0.50:
        band = "review"
    else:
        band = "hold"
    return packet, rule, band, "classed", suas, promote, forecast, conf


def as_gateway(questions):
    out = {}
    for k, q in questions.items():
        item = dict(q)
        if item.get("type") == "noul":
            item["type"] = "boolean"
        out[k] = item
    return out


def post(url, payload, token):
    raw = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=raw,
        headers={"Content-Type": "application/json", "Authorization": f"Bearer {token}"},
        method="POST",
    )
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            return json.loads(resp.read().decode("utf-8"))
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", errors="replace")[:400]
        raise RuntimeError(f"{exc.code} {url}: {detail}") from exc


def call_jev(state):
    ts = os.environ.get("TYPESAFE_API_KEY") or os.environ.get("JEV_API_KEY")
    gw = os.environ.get("AI_GATEWAY_API_KEY") or os.environ.get("VERCEL_OIDC_TOKEN")
    if ts:
        body = post(TYPESAFE_URL, {"model": "jev-latest", "state": state, "questions": QUESTIONS}, ts)
        return body, "jev-latest"
    if gw:
        body = post(
            GATEWAY_URL,
            {
                "model": "typesafe-ai/jev",
                "state": state,
                "questions": as_gateway(QUESTIONS),
                "providerOptions": {"gateway": {"zeroDataRetention": True}},
            },
            gw,
        )
        return body, "typesafe-ai/jev"
    raise RuntimeError("no Jev credential in environment")


def main():
    if not (
        os.environ.get("TYPESAFE_API_KEY")
        or os.environ.get("JEV_API_KEY")
        or os.environ.get("AI_GATEWAY_API_KEY")
        or os.environ.get("VERCEL_OIDC_TOKEN")
    ):
        print(json.dumps({"schema": "jev.evaluate.v0.live", "status": "NOT_COMPUTABLE", "reason": "missing_key"}))
        return 2

    rows = []
    model = None
    errors = []
    for case in CASES:
        try:
            raw, model = call_jev(case["state"])
            answers = raw.get("answers") or raw
            packet, rule, band, reason, suas, promote, forecast, conf = apply_policy(answers)
            row = {
                "id": case["id"],
                "pred_packet": packet,
                "gold_packet": case["gold_packet"],
                "packet_ok": packet == case["gold_packet"],
                "pred_rule": rule,
                "gold_rule": case["gold_rule"],
                "rule_ok": rule == case["gold_rule"],
                "band": band,
                "reason": reason,
                "forecast_noul": forecast,
                "promote_noul": promote,
                "suas_noul": suas,
                "packet_confidence": conf,
                "veto_ok": True,
            }
            if case.get("expect_forecast_veto"):
                row["veto_ok"] = rule == "R004"
            if case.get("expect_promote_hold"):
                row["veto_ok"] = rule == "REJECT_OR_SHADOW"
            if case.get("expect_suas_drop"):
                row["veto_ok"] = reason == "suas_drop"
            rows.append(row)
        except Exception as exc:
            errors.append({"id": case["id"], "error": str(exc)[:240]})
            rows.append(
                {
                    "id": case["id"],
                    "pred_packet": "",
                    "gold_packet": case["gold_packet"],
                    "packet_ok": False,
                    "pred_rule": "",
                    "gold_rule": case["gold_rule"],
                    "rule_ok": False,
                    "band": "hold",
                    "reason": "call_failed",
                    "veto_ok": False,
                }
            )

    n = len(rows)
    receipt = {
        "schema": "jev.evaluate.v0.live",
        "lane": "SHADOW",
        "runner": "live_eval.py",
        "model": model,
        "n": n,
        "packet_acc": round(sum(1 for r in rows if r.get("packet_ok")) / n, 4) if n else 0.0,
        "rule_acc": round(sum(1 for r in rows if r.get("rule_ok")) / n, 4) if n else 0.0,
        "veto_acc": round(sum(1 for r in rows if r.get("veto_ok")) / n, 4) if n else 0.0,
        "integrity_written": False,
        "errors": errors,
        "rows": rows,
    }
    print(json.dumps(receipt, indent=2))
    return 0 if not errors else 1


if __name__ == "__main__":
    sys.exit(main())
