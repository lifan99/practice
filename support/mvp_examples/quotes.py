"""Check a citation span without treating it as evidence of factual correctness."""

# Adapted from the MVP contracts reading; see SOURCES.json.


def validate_quote(original, finding):
    """Validate only the supplied citation fields against the unchanged text."""
    start, end, quote = finding["start"], finding["end"], finding["quote"]
    if type(start) is not int or type(end) is not int:
        raise ValueError("Offsets must be integers, excluding booleans")
    if not 0 <= start < end <= len(original):
        raise ValueError("Invalid citation range")
    if not isinstance(quote, str) or not quote.strip():
        raise ValueError("A citation must contain nonblank text")
    if original[start:end] != quote:
        raise ValueError("Citation text does not match its offsets")


def main():
    """Verify a valid citation and reject independently corrupted fields."""
    original = "仅用内存保存记录，重启后历史仍在。"
    good = {"start": 9, "end": 16, "quote": "重启后历史仍在"}
    validate_quote(original, good)
    bad_changes = [
        {"start": 8}, {"start": True}, {"end": 99}, {"quote": "已经持久化"},
    ]
    for change in bad_changes:
        try:
            validate_quote(original, {**good, **change})
        except ValueError:
            pass
        else:
            raise AssertionError(f"Expected rejection: {change}")
    repeated = "甲甲"
    validate_quote(repeated, {"start": 1, "end": 2, "quote": "甲"})
    assert repeated[1:2] == "甲"
    print("Citation checks passed: exact span, invalid fields, repeated text.")


if __name__ == "__main__":
    main()
