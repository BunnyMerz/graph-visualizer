from queue import PriorityQueue

q = PriorityQueue()

q.put((1,3))
q.put((2,2))
q.put((2,4))
q.put((2,4))
q.put((3,1))

print(q.queue)