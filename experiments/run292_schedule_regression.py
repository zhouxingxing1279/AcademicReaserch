"""Independent measurement-opportunity phase regression; not a formal automaton certification."""

def receive(step, pattern, interval=5):
    if step < 1 or interval < 1:
        raise ValueError('step and interval must be positive')
    if pattern not in ('all','MMS','SMM','SMS'):
        raise ValueError('unknown pattern')
    if step % interval:
        return False
    opportunity = step // interval - 1
    return pattern == 'all' or pattern[opportunity % len(pattern)] == 'S'

def main():
    expected={'all':30,'MMS':10,'SMM':10,'SMS':20}
    for pattern,count in expected.items():
        observed=sum(receive(k,pattern) for k in range(1,151))
        assert observed == count, (pattern,observed)
        first=''.join('S' if receive(5*i,pattern) else 'M' for i in range(1,7))
        assert first == ('SSSSSS' if pattern=='all' else pattern*2), (pattern,first)
        print(f'{pattern}: {observed}/30 received, first six={first}')
    assert not any(receive(k,'all') for k in range(1,151) if k%5)
    print('PASS: 4 patterns, phase and off-opportunity assertions')
if __name__=='__main__': main()
