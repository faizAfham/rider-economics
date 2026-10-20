"""Every number in memo.html comes from here. Sources for each input are in sources.md.

    python3 calc.py
"""
# --- disclosed (Q1 FY27, quarter ended 30 Jun 2026) ---
SWIGGY = dict(gov=9490, adj_rev=2470, cm_pct=7.6, ebitda_pct=3.1)    # Rs cr, % of GOV
ETERNAL = dict(nov=10769, adj_rev=3537, cm_pct=10.2, ebitda_pct=5.6)  # Rs cr, % of NOV
PLATFORM_FEE = 17.58          # Rs per order incl GST, both apps, Mar 2026
OWNLY_FEE = 30                # Rs per order, paid by customer; restaurants pay 0
SWISH_AOV = (200, 250)        # Rs, Swish own-kitchen basket, Mar 2026
SWISH_ORDERS_MONTH = 1_000_000   # "over 1M orders a month", Sep 2026
SEP26_RAISE_CR = 224.54       # Rs cr, Series B extension, Sep 2026
BBHA_RANGE = (8, 28)          # % commission restaurants say they pay

# --- assumptions (A) ---
PAY = 0.015                   # payment cost, share of order
SUPPORT = 0.02                # refunds + support, share of order
RIDERS = (30, 40, 50)         # Rs per Go order


def breakeven(aov, rider):
    """Commission at which a Rs 0-fee order covers its own variable cost."""
    return rider / aov + PAY + SUPPORT


def per_order(aov, rider, commission):
    return commission * aov - rider - (PAY + SUPPORT) * aov


take_s = SWIGGY["adj_rev"] / SWIGGY["gov"] * 100
take_e = ETERNAL["adj_rev"] / ETERNAL["nov"] * 100
print(f"Swiggy  take {take_s:.1f}% of GOV, keeps {SWIGGY['cm_pct']}%, so variable cost ~{take_s - SWIGGY['cm_pct']:.1f}%")
print(f"Eternal take {take_e:.1f}% of NOV, keeps {ETERNAL['cm_pct']}%, so variable cost ~{take_e - ETERNAL['cm_pct']:.1f}%")
aov = sum(SWISH_AOV) / 2
print(f"Platform fee alone = {PLATFORM_FEE / aov:.1%} of a Rs {aov:.0f} basket")

print("\nBreak-even commission  (rows: basket, cols: rider Rs 30/40/50)")
table = {a: [breakeven(a, r) for r in RIDERS] for a in (200, 225, 300, 400)}
for a, row in table.items():
    print(f"  Rs {a}: " + "  ".join(f"{v:.1%}" for v in row))

loss = per_order(aov, 40, 0.15)
monthly = loss * SWISH_ORDERS_MONTH / 1e7
print(f"\nAt 15% commission, Rs 40 rider, Rs {aov:.0f} basket: Rs {loss:.1f} per order")
print(f"If Go matched Swish's whole volume (1M/month): Rs {monthly:.2f} cr/month, "
      f"{-monthly * 12 / SEP26_RAISE_CR:.1%} of the Sep 2026 raise per year")
print(f"Go revenue per order at 15%: Rs {0.15 * aov:.2f} vs Ownly's Rs {OWNLY_FEE} delivery fee")

# sanity checks
assert round(take_s, 1) == 26.0 and round(take_e, 1) == 32.8          # matches the agents' derivation
assert all(row == sorted(row) for row in table.values())              # dearer rider -> higher commission
assert table[400][1] < table[225][1] < table[200][1]                  # bigger basket -> lower commission
assert abs(per_order(aov, 40, breakeven(aov, 40))) < 1e-9             # break-even means zero
