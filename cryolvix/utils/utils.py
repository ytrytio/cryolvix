from datetime import datetime

def format_time(seconds: float):
    return datetime.fromtimestamp(seconds).time().isoformat('seconds')

def old_format_num(num: float) -> str:
    whole, fraction = f"{num:.2f}".split(".")
    whole_with_dots = f"{int(whole):,}"
    return f"{whole_with_dots}.{fraction}"
    

def format_num(num: float) -> str:
    if num == int(num):
        num_int = int(num)
        if num_int >= 1_000_000_000_000 and int(str(surplus := num_int % 1_000_000_000_000)[0]) <= 9:
            return f"{num_int // 1_000_000_000_000}{('.'+str(surplus)[0]) if int(str(surplus)[0]) > 0 else ''}T"
        if num_int >= 1_000_000_000 and int(str(surplus := num_int % 1_000_000_000)[0]) <= 9:
            return f"{num_int // 1_000_000_000}{('.'+str(surplus)[0]) if int(str(surplus)[0]) > 0 else ''}B"
        if num_int >= 1_000_000 and int(str(surplus := num_int % 1_000_000)[0]) <= 9:
            return f"{num_int // 1_000_000}{('.'+str(surplus)[0]) if int(str(surplus)[0]) > 0 else ''}M"
        if num_int >= 1_000 and int(str(surplus := num_int % 1_000)[0]) <= 9:
            return f"{num_int // 1_000}{('.'+str(surplus)[0]) if int(str(surplus)[0]) > 0 else ''}K"
            
    return old_format_num(num)

def _button_repr(btn):
    try:
        cls = btn.__class__.__name__
        parts = []
        if hasattr(btn, "text"):
            parts.append(f"text={btn.text!r}")
        if hasattr(btn, "callback_data"):
            parts.append(f"callback_data={btn.callback_data!r}")
        if hasattr(btn, "icon_custom_emoji_id"):
            parts.append(f"icon_custom_emoji_id={btn.icon_custom_emoji_id!r}")
        return f"{cls}({', '.join(parts)})"
    except Exception:
        return repr(btn)


def pretty_print_structure(obj, indent=0):
    from cryolvix.config import CustomInlineButton
    pad = " " * indent

    if isinstance(obj, list):
        if not obj:
            print(pad + "[]")
            return

        if all(not isinstance(i, list) for i in obj) and len(obj) <= 6:
            inner = ", ".join(
                _button_repr(i) if not isinstance(i, list) else "[...]" for i in obj
            )
            print(pad + f"[{inner}]")
            return
        print(pad + "[")
        for item in obj:
            pretty_print_structure(item, indent + 4)
        print(pad + "]")

    elif isinstance(obj, CustomInlineButton):
        print(pad + _button_repr(obj))

    elif isinstance(obj, dict):
        print(pad + "{")
        for k, v in obj.items():
            print(pad + f"    {k!r}: ", end="")
            pretty_print_structure(v, indent + 8)
        print(pad + "}")
    else:
        print(pad + repr(obj))
