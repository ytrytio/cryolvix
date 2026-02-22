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
