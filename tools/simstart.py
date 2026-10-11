"""startup-faithful init for sim6: edges that occur before a block runs are lost (BLatch.changed checks isRunning)."""
def faithful(m):
    m.settle()
    for n, s in m.st.items():
        t = m.typ(n)
        if t in ('BooleanLatch', 'NumericLatch'): s['clk'] = bool(m.g(n, 'clock', False))
        if t == 'Counter': s['up'] = bool(m.g(n, 'countUp', False)); s['clr'] = bool(m.g(n, 'clearIn', False))
    for n in m.C:
        if m.typ(n) == 'BooleanLatch': m.out[n] = False
    return m
