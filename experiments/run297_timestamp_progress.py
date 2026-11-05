"""Finite-prefix counterexample: arrivals do not guarantee timestamp progress."""
def ages(deliveries):
    newest = -1
    out = []
    for k, stamps in enumerate(deliveries):
        for stamp in stamps:
            assert 0 <= stamp <= k
            newest = max(newest, stamp)
        out.append(None if newest < 0 else k - newest)
    return out

if __name__ == "__main__":
    for n in (10, 100, 1000):
        repeated = ages([[0] for _ in range(n)])
        fresh = ages([[k] for k in range(n)])
        delayed = ages([([k - 1] if k % 2 else []) for k in range(n)])
        assert repeated[-1] == n - 1
        assert max(fresh) == 0
        assert max(a for a in delayed if a is not None) <= 2
        print(f"n={n} repeated_old_age={repeated[-1]} fresh_age=0 delayed_age_bound={max(a for a in delayed if a is not None)}")
    print("PASS: timestamp-age counterexample and bounded-delay sanity check")
