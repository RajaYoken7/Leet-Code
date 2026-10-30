import heapq

class Solution:
    def shortestPath(self, n, edges, labels, k):

        # -----------------------------------------
        # STEP 1: CREATE THE ADJACENCY MATRIX
        # -----------------------------------------

        # Initially, assume there is no edge
        # between any pair of nodes.
        # float('inf') represents infinity.
        adj = [[float('inf')] * n for _ in range(n)]

        # Store the directed edges and their weights.
        for u, v, w in edges:

            # Edge from node u to node v has weight w.
            adj[u][v] = w

        # -----------------------------------------
        # STEP 2: CREATE THE DISTANCE MATRIX
        # -----------------------------------------

        # dist[node][count] represents:
        # Minimum cost to reach 'node'
        # with 'count' consecutive identical characters.
        #
        # We need k + 1 columns because counts range
        # from 0 to k. Column 0 is unused.
        dist = [[float('inf')] * (k + 1) for _ in range(n)]

        # We start at node 0.
        # Its character has already appeared once.
        # The cost of starting is 0.
        dist[0][1] = 0

        # -----------------------------------------
        # STEP 3: CREATE THE PRIORITY QUEUE
        # -----------------------------------------

        # Priority queue stores:
        # (cost, node, consecutive_count)
        pq = []

        # Initially, we are at node 0.
        # Cost = 0, Node = 0, Count = 1.
        heapq.heappush(pq, (0, 0, 1))

        # -----------------------------------------
        # STEP 4: DIJKSTRA'S ALGORITHM
        # -----------------------------------------

        # Continue until the priority queue becomes empty.
        while pq:

            # Extract the state with the minimum cost.
            cost, node, count = heapq.heappop(pq)

            # Check whether this is an outdated state.
            # If a cheaper path was already found,
            # we don't need to process this state.
            if cost > dist[node][count]:
                continue

            # -----------------------------------------
            # STEP 5: VISIT ALL NEIGHBOURING NODES
            # -----------------------------------------

            # Check every possible node in the graph.
            for i in range(n):

                # Check whether an edge exists
                # from the current node to node i.
                if adj[node][i] != float('inf'):

                    # ---------------------------------
                    # STEP 6: UPDATE CONSECUTIVE COUNT
                    # ---------------------------------

                    # Compare the current node's character
                    # with the next node's character.
                    if labels[node] == labels[i]:

                        # Same character:
                        # Increase consecutive count.
                        new_count = count + 1

                    else:

                        # Different character:
                        # Reset consecutive count to 1.
                        new_count = 1

                    # ---------------------------------
                    # STEP 7: CHECK THE CONSTRAINT
                    # ---------------------------------

                    # If consecutive count exceeds k,
                    # this path is invalid.
                    if new_count > k:
                        continue

                    # ---------------------------------
                    # STEP 8: CALCULATE NEW PATH COST
                    # ---------------------------------

                    # Previous path cost + edge weight.
                    new_cost = cost + adj[node][i]

                    # ---------------------------------
                    # STEP 9: RELAXATION
                    # ---------------------------------

                    # Check whether the newly discovered
                    # path is cheaper than the old path.
                    if new_cost < dist[i][new_count]:

                        # Update the minimum distance.
                        dist[i][new_count] = new_cost

                        # Push the improved state into
                        # the priority queue.
                        heapq.heappush(
                            pq,
                            (new_cost, i, new_count)
                        )

        # -----------------------------------------
        # STEP 10: FIND THE FINAL ANSWER
        # -----------------------------------------

        # Destination node is n - 1.
        #
        # It may be reached with different consecutive
        # counts, so find the minimum among all valid counts.
        ans = min(dist[n - 1][1:])

        # If destination is unreachable, return -1.
        if ans == float('inf'):
            return -1

        # Otherwise, return the minimum cost.
        return ans
