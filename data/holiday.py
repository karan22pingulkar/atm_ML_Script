import holidays

h = holidays.country_holidays("IN", years=[2026])

for d, name in sorted(h.items()):
    print(d, name)