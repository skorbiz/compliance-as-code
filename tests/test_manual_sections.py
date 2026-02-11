def test_manual_includes_required_sections():
    with open("docs/manual.typ") as f:
        content = f.read()

    required_headings = [
        "= Commissioning",
        "= Operation",
        "= Decommissioning",
    ]

    for heading in required_headings:
        assert heading in content, f"Missing manual section: {heading}"
