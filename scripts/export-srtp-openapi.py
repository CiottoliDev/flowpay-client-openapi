#!/usr/bin/env python3
"""Export the SRTP contract and its transitive component dependencies."""

import copy
import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def export(source):
    document = {
        key: copy.deepcopy(source[key])
        for key in ("openapi", "info", "servers", "security")
    }
    document["info"]["title"] = "FlowPay SRTP Payees API"
    document["info"]["description"] = (
        "Proposed SRTP payees contract for the FlowPay client gateway. "
        "Preserves pagoPA payee data with standard FlowPay limit/offset pagination, "
        "API-key authentication and gateway errors. This document does not confirm "
        "runtime availability."
    )
    document["tags"] = [copy.deepcopy(tag) for tag in source["tags"] if tag["name"] == "SRTP"]
    document["paths"] = {
        path: copy.deepcopy(item)
        for path, item in source["paths"].items()
        if path.startswith("/srtp/")
    }
    if not document["paths"]:
        raise ValueError("No SRTP paths found")
    document["components"] = {}
    pending = []

    def collect(value):
        if isinstance(value, dict):
            if "$ref" in value:
                ref = value["$ref"]
                if not ref.startswith("#/components/"):
                    raise ValueError(f"Non-component reference in standalone document: {ref}")
                pending.append(ref)
            # Security requirements name schemes without using $ref.
            for requirement in value.get("security", []):
                pending.extend(f"#/components/securitySchemes/{name}" for name in requirement)
            for child in value.values():
                collect(child)
        elif isinstance(value, list):
            for child in value:
                collect(child)

    collect(document)
    seen = set()
    while pending:
        ref = pending.pop(0)
        if ref in seen:
            continue
        seen.add(ref)
        _, _, category, name = ref.split("/")
        component = copy.deepcopy(source["components"][category][name])
        document["components"].setdefault(category, {})[name] = component
        collect(component)
    return document


if __name__ == "__main__":
    source = json.loads((ROOT / "openapi.json").read_text())
    target = ROOT / "docs" / "srtp-openapi.json"
    target.write_text(json.dumps(export(source), indent=4, ensure_ascii=False) + "\n")
    print(target.relative_to(ROOT))
