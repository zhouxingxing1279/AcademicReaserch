from collections import deque

def explore(H=2, D=2):
    # (consecutive failed generations, ages of pending deliveries, newest delivered age)
    initial = (0, (), None)
    frontier = {initial}
    seen = {initial}
    edges = 0
    max_age = 0
    for k in range(25):
        nxt = set()
        for miss, pending, age in frontier:
            for success in (False, True):
                if not success and miss >= H:
                    continue
                samples = tuple(a + 1 for a in pending) + ((0,) if success else ())
                for mask in range(1 << len(samples)):
                    if any(a >= D and not (mask >> i & 1) for i, a in enumerate(samples)):
                        continue
                    delivered = [a for i, a in enumerate(samples) if mask >> i & 1]
                    remains = tuple(a for i, a in enumerate(samples) if not (mask >> i & 1))
                    candidates = ([age + 1] if age is not None else []) + delivered
                    new_age = min(candidates) if candidates else None
                    state = (0 if success else miss + 1, remains, new_age)
                    edges += 1
                    if k >= H + D and new_age is not None:
                        assert new_age <= H + D, (k, state)
                        max_age = max(max_age, new_age)
                    nxt.add(state)
                    seen.add(state)
        frontier = nxt
    print(dict(H=H, D=D, reachable_states=len(seen), edges=edges, max_age=max_age))

if __name__ == "__main__":
    for h, d in ((0, 0), (1, 1), (2, 2), (3, 2)):
        explore(h, d)
