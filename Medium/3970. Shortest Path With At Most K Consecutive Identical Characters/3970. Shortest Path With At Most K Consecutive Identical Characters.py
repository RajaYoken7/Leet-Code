import heapq

class Solution:
    def shortestPath(self, n, edges, labels, k):

        adj = [[] for _ in range(n)]

        for u, v, w in edges:
            adj[u].append((v, w))

        dist = [[float('inf')] * (k + 1) for _ in range(n)]

      
        dist[0][1] = 0

 
        pq = []
        heapq.heappush(pq, (0, 0, 1))

     
        while pq:

            cost, node, count = heapq.heappop(pq)

      
            if cost > dist[node][count]:
                continue

            for i, weight in adj[node]:

  
                if labels[node] == labels[i]:
                    new_count = count + 1
                else:
                    new_count = 1

 
                if new_count > k:
                    continue

                new_cost = cost + weight

                if new_cost < dist[i][new_count]:

                    dist[i][new_count] = new_cost

                    heapq.heappush(
                        pq,
                        (new_cost, i, new_count)
                    )

        ans = min(dist[n - 1][1:])

        if ans == float('inf'):
            return -1

        return ans
