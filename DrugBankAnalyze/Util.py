def is_valid_drugbank_id(id : str) -> bool:
    return len(id) == 7 and id[:2] == "DB" and id[2:].isdigit()

def cap_str(s : str, max_len : int) -> str:
    assert max_len > 3
    return s[:max_len - 3] + "..." if len(s) > max_len else s

def autopct_gen(treshold=5):
    return lambda pct: f"{pct:.1f}%" if pct >= treshold else ""