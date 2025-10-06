import random, time, itertools

# generate a random 3-SAT instance

def make_3sat(n, m):
clauses = []
while len(clauses) < m:
vars_ = random.sample(range(1, n+1), 3)
lits = []
for v in vars_:
lits.append(v if random.random() < 0.5 else -v)
if lits not in clauses:
clauses.append(tuple(lits))
return clauses

# evaluate assignment

def eval_assign(clauses, assign):
sat = 0
unsat = 0
counts = []
for c in clauses:
t = 0
for lit in c:
var = abs(lit)-1
val = assign[var]
if lit < 0: val = not val
if val: t += 1
if t > 0:
sat += 1
else:
unsat += 1
counts.append(t)
return sat, unsat, counts

def is_sat(clauses, assign):
return eval_assign(clauses, assign)[1] == 0

# heuristics

def h1(clauses, assign):
return eval_assign(clauses, assign)[0]

def h2(clauses, assign):
sat, _, counts = eval_assign(clauses, assign)
score = 0
for c in counts:
if c > 0:
score += 1.0/c
return score

# helpers

def flip(assign, idxs):
new = assign[:]
for i in idxs:
new[i] = not new[i]
return new

# Hill Climbing

def hill_climb(clauses, n, heur, max_steps=2000, restarts=3):
steps = 0
start = time.time()
for r in range(restarts):
a = [random.choice([True, False]) for _ in range(n)]
best = heur(clauses, a)
for s in range(max_steps):
steps += 1
moves = []
for i in range(n):
a2 = flip(a, [i])
val = heur(clauses, a2)
if val > best:
moves.append((val,i))
if not moves: break
_, pick = random.choice(moves)
a = flip(a,[pick])
best = heur(clauses, a)
if is_sat(clauses,a):
return True, steps, time.time()-start
return False, steps, time.time()-start

# Beam Search

def beam_search(clauses, n, heur, width=3, max_exp=2000):
beam = []
for _ in range(width):
a = [random.choice([True, False]) for _ in range(n)]
beam.append((heur(clauses,a),a))
exp = 0
start = time.time()
while exp < max_exp:
for h,a in beam:
if is_sat(clauses,a):
return True, exp, time.time()-start
cands = []
for h,a in beam:
for i in range(n):
a2 = flip(a,[i])
exp += 1
cands.append((heur(clauses,a2),a2))
if exp>=max_exp: break
if exp>=max_exp: break
cands.sort(key=lambda x: -x[0])
beam = cands[:width]
return False, exp, time.time()-start

# VND

def vnd(clauses, n, heur, max_steps=2000):
a = [random.choice([True, False]) for _ in range(n)]
cur = heur(clauses,a)
steps = 0
start = time.time()
while steps < max_steps:
improved = False
for k in [1,2,3]:
if k==1:
neighs = [[i] for i in range(n)]
else:
combos = list(itertools.combinations(range(n),k))
if len(combos) > 200:
combos = random.sample(combos,200)
neighs = combos
best = cur
besta = None
for idxs in neighs:
a2 = flip(a,idxs)
val = heur(clauses,a2)
steps += 1
if val > best:
best = val
besta = a2
if steps>=max_steps: break
if besta:
a = besta
cur = best
improved = True
break
if not improved: break
return is_sat(clauses,a), steps, time.time()-start

# run experiment

def run_all(ns=[20], ratios=[4.2], inst=3, runs=3):
algs = ["hill","beam3","beam4","vnd"]
heurs = [h1,h2]
results = []
for n in ns:
for r in ratios:
m = int(r*n)
for t in range(inst):
clauses = make_3sat(n,m)
for alg in algs:
for heur in heurs:
succ = 0
for run in range(runs):
if alg=="hill":
ok,steps,tim = hill_climb(clauses,n,heur)
elif alg=="beam3":
ok,steps,tim = beam_search(clauses,n,heur,3)
elif alg=="beam4":
ok,steps,tim = beam_search(clauses,n,heur,4)
else:
ok,steps,tim = vnd(clauses,n,heur)
if ok: succ+=1
pen = succ/runs
results.append((n,m,alg,heur.**name**,pen))
print(f"n={n}, m={m}, alg={alg}, heur={heur.**name**}, penetrance={pen:.2f}")
return results

if **name**=="**main**":
run_all(ns=[20,50],ratios=[3.3,4.2],inst=2,runs=3)
