# Shortest Path With At Most K Consecutive Identical Characters

## A beginner-friendly, line-by-line guide

This README explains the Python solution slowly and simply. Imagine that
you are teaching the algorithm to someone who has never studied graphs
before.

------------------------------------------------------------------------

# 1. First understand the problem

You are given:

-   `n`: how many nodes (places) are in the graph.
-   `edges`: roads connecting nodes. Each road is written as
    `[u, v, w]`.
    -   `u` = where the road starts.
    -   `v` = where the road goes.
    -   `w` = the cost of travelling along that road.
-   `labels`: a string. The character at position `i` belongs to node
    `i`.
-   `k`: the largest allowed number of identical characters in a row.

You must travel from node `0` to node `n - 1`.

While travelling, look at the characters of the nodes you visit. You are
not allowed to visit more than `k` identical characters consecutively.

Among all paths that obey this rule, return the one with the smallest
total edge cost. If no valid path exists, return `-1`.

## A tiny example

``` python
n = 3
edges = [[0, 1, 1], [1, 2, 1], [0, 2, 3]]
labels = "aab"
k = 1
```

The nodes have these labels:

  Node   Label
  ------ -------
  0      a
  1      a
  2      b

Possible paths:

-   `0 -> 1 -> 2` spells `aab`. It has two `a` characters in a row.
    Since `k = 1`, this path is invalid.
-   `0 -> 2` spells `ab`. No character repeats consecutively. Its cost
    is `3`.

So the answer is `3`.

------------------------------------------------------------------------

# 2. The complete code

Read the explanations in the next sections while looking at this code.

``` python
import heapq

class Solution:
    def shortestPath(self, n, edges, labels, k):

        # STEP 1: Build an adjacency list.
        adj = [[] for _ in range(n)]

        for u, v, w in edges:
            adj[u].append((v, w))

        # STEP 2: Store the best known cost for each state.
        dist = [[float('inf')] * (k + 1) for _ in range(n)]

        # STEP 3: Set the starting state.
        dist[0][1] = 0

        # STEP 4: Create a min-priority queue.
        pq = []
        heapq.heappush(pq, (0, 0, 1))

        # STEP 5: Run Dijkstra's algorithm.
        while pq:

            cost, node, count = heapq.heappop(pq)

            # Ignore an old, more expensive queue entry.
            if cost > dist[node][count]:
                continue

            # STEP 6: Visit each real neighbour of this node.
            for i, weight in adj[node]:

                # STEP 7: Work out the new consecutive count.
                if labels[node] == labels[i]:
                    new_count = count + 1
                else:
                    new_count = 1

                # STEP 8: Reject a path that breaks the rule.
                if new_count > k:
                    continue

                # STEP 9: Calculate the cost of this new path.
                new_cost = cost + weight

                # STEP 10: Keep the path only if it is cheaper.
                if new_cost < dist[i][new_count]:

                    dist[i][new_count] = new_cost

                    # STEP 11: Schedule this improved state to explore.
                    heapq.heappush(pq, (new_cost, i, new_count))

        # STEP 12: Choose the cheapest valid way to reach the destination.
        ans = min(dist[n - 1][1:])

        if ans == float('inf'):
            return -1

        return ans
```

------------------------------------------------------------------------

# 3. Line-by-line explanation

## Line 1

``` python
import heapq
```

`heapq` is a Python tool that gives us a priority queue.

Think of a queue at a shop:

-   In a normal queue, the first person who arrives is served first.
-   In a priority queue here, the state with the smallest travel cost is
    taken first.

Dijkstra's algorithm needs us to explore the cheapest available path
first.

## Line 2

``` python
class Solution:
```

LeetCode expects the solution to be inside a class named `Solution`.

A class is like a container that holds related functions.

Do not change this name when submitting to LeetCode unless the problem
asks for something different.

## Line 3

``` python
def shortestPath(self, n, edges, labels, k):
```

This creates the function that solves the problem.

The inputs are:

-   `self`: Python uses this when a function belongs to a class.
-   `n`: number of nodes.
-   `edges`: roads and their costs.
-   `labels`: one character for each node.
-   `k`: maximum allowed consecutive identical characters.

The function eventually returns an integer: the minimum cost, or `-1`.

------------------------------------------------------------------------

# 4. Step 1 --- Build the adjacency list

``` python
adj = [[] for _ in range(n)]
```

We need a way to remember which nodes are connected.

An adjacency list is like a contact list:

-   `adj[0]` stores the neighbours of node `0`.
-   `adj[1]` stores the neighbours of node `1`.
-   `adj[2]` stores the neighbours of node `2`.

The expression creates `n` empty lists.

For example, if `n = 3`, it creates:

``` python
adj = [
    [],
    [],
    []
]
```

Every node starts with an empty neighbour list.

## Read every edge

``` python
for u, v, w in edges:
```

This takes one edge at a time.

Suppose:

``` python
edges = [
    [0, 1, 5],
    [0, 2, 3],
    [1, 2, 4]
]
```

On the first loop:

``` text
u = 0
v = 1
w = 5
```

On the second loop:

``` text
u = 0
v = 2
w = 3
```

On the third loop:

``` text
u = 1
v = 2
w = 4
```

Python automatically unpacks the three values into `u`, `v`, and `w`.

## Store the edge

``` python
adj[u].append((v, w))
```

This means:

"Inside the neighbour list of node `u`, add the destination node `v` and
the road cost `w`."

For the example above, the final adjacency list is:

``` python
adj = [
    [(1, 5), (2, 3)],
    [(2, 4)],
    []
]
```

Read it like this:

-   From node `0`, we can go to node `1` with cost `5`, or node `2` with
    cost `3`.
-   From node `1`, we can go to node `2` with cost `4`.
-   From node `2`, there are no outgoing edges.

### Important: the graph is directed

For an edge `[0, 1, 5]`, we can travel from `0` to `1`.

We cannot automatically travel from `1` to `0`.

That is why we only write:

``` python
adj[u].append((v, w))
```

We do not also add the reverse edge.

### What about duplicate edges?

If the input has two edges from the same source to the same destination,
both are stored. Dijkstra can examine both. The cheaper one can improve
the distance; the more expensive one will not replace a cheaper result.

------------------------------------------------------------------------

# 5. Step 2 --- Create the distance table

``` python
dist = [[float('inf')] * (k + 1) for _ in range(n)]
```

This is the most important idea in the problem.

A normal shortest-path problem asks:

"What's the cheapest cost to reach node 3?"

This problem needs one extra piece of information:

"What's the cheapest cost to reach node 3 when the current
consecutive-character count is 1? What about when it is 2? What about
when it is 3?"

So we need a table with:

-   Rows = nodes.
-   Columns = consecutive counts.

We call a combination of a node and a count a **state**.

For example:

``` python
dist[3][1]
```

means:

"The cheapest cost found so far to reach node 3 with a consecutive count
of 1."

And:

``` python
dist[3][2]
```

means:

"The cheapest cost found so far to reach node 3 with a consecutive count
of 2."

## Why `k + 1` columns?

Suppose `k = 3`.

The possible counts are:

``` text
0, 1, 2, 3
```

That is four columns, so we create `k + 1` columns.

Column `0` is not used. A visited node always contributes at least one
character, so a valid count starts at `1`.

## What does infinity mean?

``` python
float('inf')
```

means infinity.

We use it as the starting value because we have not found a path to that
state yet.

For `n = 3` and `k = 2`, the table starts like this:

``` text
          count 0    count 1    count 2
node 0      inf        inf        inf
node 1      inf        inf        inf
node 2      inf        inf        inf
```

It says: "We do not know a route to any state yet."

------------------------------------------------------------------------

# 6. Step 3 --- Set the starting state

``` python
dist[0][1] = 0
```

We begin at node `0`.

Why is the count `1`?

Because the starting node already has a character.

For example, if `labels = "aab"`, node `0` has label `a`. Before
travelling anywhere, we have already seen one `a`.

Why is the cost `0`?

Because we have not travelled along any edge yet.

So:

``` python
dist[0][1] = 0
```

means:

"Reaching node 0 with one character in the current consecutive group
costs zero."

All other states remain infinity until we discover paths to them.

------------------------------------------------------------------------

# 7. Step 4 --- Create the priority queue

``` python
pq = []
```

This creates an empty priority queue.

Next:

``` python
heapq.heappush(pq, (0, 0, 1))
```

This inserts the starting state.

Every state is stored as a tuple with three values:

``` text
(cost, node, count)
```

For example:

``` python
(0, 0, 1)
```

means:

-   Cost = `0`.
-   Current node = `0`.
-   Consecutive count = `1`.

Remember this order. It is used throughout the algorithm.

------------------------------------------------------------------------

# 8. Step 5 --- Keep working while the queue has states

``` python
while pq:
```

This means:

"Repeat the following steps while the priority queue is not empty."

At the beginning, the queue contains:

``` python
[(0, 0, 1)]
```

After exploring neighbours, new states may be inserted.

The loop continues until there is nothing left to explore.

## Take the cheapest state

``` python
cost, node, count = heapq.heappop(pq)
```

`heappop` removes and returns the smallest tuple.

Python compares tuples from left to right. Since cost is the first
value, the smallest-cost state is normally removed first.

The three values are placed into variables:

-   `cost`: current total path cost.
-   `node`: current node.
-   `count`: current consecutive count.

For example, if the removed tuple is:

``` python
(7, 2, 1)
```

then:

``` text
cost = 7
node = 2
count = 1
```

------------------------------------------------------------------------

# 9. Ignore an outdated state

``` python
if cost > dist[node][count]:
    continue
```

Sometimes we discover a route and put it into the queue.

Later, we discover a cheaper route to the exact same state.

The old, more expensive entry may still be waiting in the queue. We do
not need to process it.

Example:

``` text
Old queue entry:       (10, 2, 1)
Best known distance:   dist[2][1] = 6
```

The queue entry costs `10`, but we already know a route costing `6`.

So:

``` python
10 > 6
```

is true, and:

``` python
continue
```

skips this outdated entry.

### Why compare the count too?

We check:

``` python
dist[node][count]
```

not just:

``` python
dist[node]
```

Reaching the same node with different consecutive counts can lead to
different valid future paths.

For example, reaching a node with count `1` may allow another identical
character. Reaching it with count `3` may not, if `k = 3`.

They are different states and must be tracked separately.

------------------------------------------------------------------------

# 10. Step 6 --- Visit the current node's neighbours

``` python
for i, weight in adj[node]:
```

Remember that `adj[node]` contains only the outgoing neighbours of the
current node.

Each item has two values:

``` text
(neighbour, edge_weight)
```

So:

-   `i` is the next node.
-   `weight` is the cost of the edge from `node` to `i`.

Example:

``` python
adj[0] = [(1, 5), (2, 3)]
```

When the current node is `0`, the loop runs twice.

First time:

``` text
i = 1
weight = 5
```

Second time:

``` text
i = 2
weight = 3
```

We do not scan all `n` nodes. We only scan actual neighbours.

------------------------------------------------------------------------

# 11. Step 7 --- Update the consecutive count

``` python
if labels[node] == labels[i]:
```

We compare the character at the current node with the character at the
next node.

-   `labels[node]` = current node's character.
-   `labels[i]` = next node's character.

## If they are the same

``` python
new_count = count + 1
```

Increase the count by one.

Example:

``` text
Current character: a
Next character:    a
Old count:         1
New count:         2
```

Another example:

``` text
Path labels so far: a, a
Next label:         a
New consecutive count: 3
```

## If they are different

``` python
else:
    new_count = 1
```

The old group of identical characters has ended.

A new group starts with the next character, so its count is `1`.

Example:

``` text
Current character: a
Next character:    b
Old count:         2
New count:         1
```

Think of the sequence:

``` text
a, a, b
```

The current consecutive group is now just `b`, so the count is `1`.

------------------------------------------------------------------------

# 12. Step 8 --- Reject an invalid path

``` python
if new_count > k:
    continue
```

The problem says that no more than `k` identical characters may appear
consecutively.

Suppose:

``` python
k = 2
```

Then:

    New count Valid?
  ----------- --------
            1 Yes
            2 Yes
            3 No

If the new count is greater than `k`, this path breaks the rule.

`continue` means:

"Do not process this neighbour any further. Move to the next neighbour."

We do not calculate its cost or put it in the priority queue.

------------------------------------------------------------------------

# 13. Step 9 --- Calculate the new cost

``` python
new_cost = cost + weight
```

This is simple addition.

-   `cost` = how much we have spent to reach the current node.
-   `weight` = cost of the next edge.
-   `new_cost` = total cost after travelling to the neighbour.

Example:

``` text
Cost so far = 7
Next edge   = 4
New cost    = 7 + 4 = 11
```

So:

``` python
new_cost = 11
```

------------------------------------------------------------------------

# 14. Step 10 --- Check whether this route is cheaper

``` python
if new_cost < dist[i][new_count]:
```

We are checking:

"Is this newly discovered route cheaper than the best route we already
know for this exact state?"

Remember, the state is:

``` text
(next node, new consecutive count)
```

Example:

``` text
New cost:                       4
Previously stored distance:    9
```

Since `4 < 9`, the new route is better.

But if:

``` text
New cost:                       12
Previously stored distance:    9
```

then the new route is worse. We do not update anything.

## Save the better cost

``` python
dist[i][new_count] = new_cost
```

This records the cheaper route in the distance table.

For example:

``` text
Before: dist[2][1] = 9
New cost: 4
After:  dist[2][1] = 4
```

Now the best known cost for that state is `4`.

------------------------------------------------------------------------

# 15. Step 11 --- Put the improved state into the queue

``` python
heapq.heappush(
    pq,
    (new_cost, i, new_count)
)
```

We have found a better way to reach a state.

We must add that state to the priority queue so that the algorithm can
explore its neighbours later.

The tuple order is still:

``` text
(cost, node, count)
```

For example:

``` python
heapq.heappush(pq, (4, 2, 1))
```

means:

-   Cost to reach the state = `4`.
-   Current node = `2`.
-   Consecutive count = `1`.

The priority queue will choose states in increasing cost order.

------------------------------------------------------------------------

# 16. Step 12 --- Find the final answer

When the `while pq` loop finishes, all reachable valid states have been
processed.

The destination node is:

``` python
n - 1
```

For example, if `n = 5`, the nodes are:

``` text
0, 1, 2, 3, 4
```

The destination is node `4`, which is `n - 1`.

## Check every valid count at the destination

``` python
ans = min(dist[n - 1][1:])
```

The destination may be reached with different consecutive counts.

For example:

``` text
dist[4][1] = 15
dist[4][2] = 10
dist[4][3] = 20
```

All three states obey the limit if `k = 3`.

The cheapest is `10`.

The slice:

``` python
dist[n - 1][1:]
```

means:

"Take the destination row, starting from column 1. Ignore column 0."

`min(...)` returns the smallest value.

## If no valid route exists

``` python
if ans == float('inf'):
    return -1
```

If the answer is still infinity, we never found a valid way to reach the
destination.

So return `-1`.

## Otherwise, return the answer

``` python
return ans
```

This gives the minimum cost of a valid path.

------------------------------------------------------------------------

# 17. Complete dry run of the small example

Input:

``` python
n = 3
edges = [
    [0, 1, 1],
    [1, 2, 1],
    [0, 2, 3]
]
labels = "aab"
k = 1
```

## First: build the adjacency list

``` python
adj = [
    [(1, 1), (2, 3)],
    [(2, 1)],
    []
]
```

## Second: initialize the distance table

Since `k = 1`, only count `1` is valid.

``` text
             count 0    count 1
node 0          inf        0
node 1          inf        inf
node 2          inf        inf
```

## Third: initialize the queue

``` python
pq = [(0, 0, 1)]
```

This means we start at node `0`, with cost `0` and count `1`.

## Fourth: remove the first state

The queue gives:

``` text
cost = 0
node = 0
count = 1
```

Node `0` has two neighbours: node `1` and node `2`.

### Try neighbour 1

``` text
labels[0] = a
labels[1] = a
```

They are the same.

``` text
new_count = 1 + 1 = 2
```

But:

``` text
k = 1
new_count = 2
```

Since `2 > 1`, reject this path.

We cannot use `0 -> 1`.

### Try neighbour 2

``` text
labels[0] = a
labels[2] = b
```

They are different.

``` text
new_count = 1
```

The new cost is:

``` text
new_cost = 0 + 3 = 3
```

The old distance is infinity, so `3` is better.

Update:

``` python
dist[2][1] = 3
```

Push:

``` python
(3, 2, 1)
```

## Fifth: remove the next state

The queue gives:

``` text
cost = 3
node = 2
count = 1
```

Node `2` is the destination. It has no outgoing neighbours.

The queue becomes empty, so the algorithm ends.

## Sixth: get the answer

``` python
ans = min(dist[2][1:])
```

The result is:

``` text
3
```

The function returns:

``` python
3
```

------------------------------------------------------------------------

# 18. Common mistakes to avoid

  -----------------------------------------------------------------------
  Mistake                             Correct idea
  ----------------------------------- -----------------------------------
  Using an `n x n` adjacency matrix   Use an adjacency list
  for a huge sparse graph             

  Forgetting that the graph is        Store only `u -> v`
  directed                            

  Storing only one distance per node  Store distance for each
                                      `(node, count)` state

  Starting with count `0`             Start with count `1`, because node
                                      0 already has a label

  Increasing count when characters    Reset count to `1`
  differ                              

  Forgetting `new_count > k`          Reject invalid paths

  Adding only the edge weight as the  Use `cost + weight`
  new cost                            

  Updating a distance when the new    Update only if
  route is more expensive             `new_cost < dist[i][new_count]`

  Pushing a state before updating its Update first, then push
  distance                            

  Returning only `dist[n-1][k]`       Take the minimum over all valid
                                      counts
  -----------------------------------------------------------------------

------------------------------------------------------------------------

# 19. Quick memory sheet

Try to remember the algorithm in this order:

1.  **Build graph** --- store each neighbour and edge weight.
2.  **Create distances** --- one distance for every node and count.
3.  **Initialize start** --- node `0`, count `1`, cost `0`.
4.  **Create heap** --- push `(0, 0, 1)`.
5.  **Pop minimum** --- get `(cost, node, count)`.
6.  **Skip old entry** --- ignore it if its cost is worse than the saved
    distance.
7.  **Visit neighbours** --- read `adj[node]`.
8.  **Update count** --- same character: add one; different character:
    reset to one.
9.  **Check limit** --- if count exceeds `k`, skip.
10. **Calculate cost** --- current cost plus edge weight.
11. **Relax and push** --- if cheaper, update distance and push the
    state.
12. **Return answer** --- minimum valid distance at node `n - 1`, or
    `-1`.

## Three questions to ask yourself while coding

1.  What does my state represent?\
    **Answer:** `(node, consecutive_count)`.

2.  What does my distance entry represent?\
    **Answer:** The minimum cost to reach that exact state.

3.  Why do I need a priority queue?\
    **Answer:** To explore the currently cheapest state first.

------------------------------------------------------------------------

# 20. Complexity

Let:

-   `V` = number of nodes (`n`).
-   `E` = number of directed edges.

The adjacency list uses `O(V + E)` space.

There are at most `V * k` useful states because each node can have
counts from `1` to `k`.

The distance table uses `O(V * k)` space.

The priority queue can hold multiple entries for improved states. A
standard upper-bound analysis for this expanded graph gives
approximately:

-   **Time:** `O((V*k + E*k) log(V*k))`
-   **Space:** `O(V*k + E)`, plus priority-queue entries.

The key memory improvement is replacing the adjacency matrix's `O(V²)`
storage with an adjacency list's `O(V + E)` storage.

------------------------------------------------------------------------

## Final advice

Do not try to memorize every comment. Understand these four ideas:

-   **Adjacency list:** Where can I go next?
-   **Distance table:** What is the cheapest cost for each state?
-   **Consecutive count:** Is this path allowed?
-   **Priority queue:** Which state should I explore next?

If you understand those four ideas, the rest of the code becomes much
easier to remember.
