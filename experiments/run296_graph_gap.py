"""Run296: finite labelled automaton fresh-measurement gap criterion."""
from collections import deque

def check(initial, edges):
    reachable={initial}; todo=deque([initial])
    while todo:
        u=todo.popleft()
        for a,b,label in edges:
            if a==u and b not in reachable:
                reachable.add(b);todo.append(b)
    adj={u:[] for u in reachable}
    for a,b,label in edges:
        if a in reachable and label!='S':
            adj[a].append(b)
    color={u:0 for u in reachable}
    def cycle(u):
        color[u]=1
        for v in adj[u]:
            if color[v]==1 or (color[v]==0 and cycle(v)):return True
        color[u]=2
        return False
    if any(color[u]==0 and cycle(u) for u in reachable):return None
    memo={}
    def length(u):
        if u not in memo:
            memo[u]=max([1+length(v) for v in adj[u]]+[0])
        return memo[u]
    return max(length(u) for u in reachable)

if __name__=='__main__':
    assert check('A',[('A','B','M'),('B','A','S')])==1
    assert check('A',[('A','B','M'),('B','A','S'),('B','B','M')]) is None
    assert check('A',[('A','B','M'),('B','C','M'),('C','A','S')])==2
    print('PASS: alternating=1; reachable miss cycle=unbounded; MMS=2')
