class linked_list():   # created linked list 
    pass
    class Node():
        def __init__(self,vertex_num,capacity,m): # the node has 3 element : vertex number , capacity , and m which is the index same as the index in a list , which I will use in heap_index (a list) .  
            self._capacity = capacity
            self._m = m
            self._vertex_num = vertex_num
            self._prev = None
            self._next = None

    def __init__(self,total_vertices,bool):    # maintained head and last for the linked list . Created a list which can store address of the elements , so wherever they are present in a heap ,they can be accessed from their addresses stored in the list.
        self._head = None
        self._last = None
        if bool == True:
            self._l = []
            for i in range (total_vertices):
                self._l.append(-1)

    def is_Empty(self):
        if self._head == None :
            return True 
        else :
            return False

    def push(self,i,y,m,bool):
        ptr = self.Node(i,y,m)
        if bool == True:
            self._l.append(ptr)
        if self._head == None:
            self._head = ptr
            self._last = ptr
        else :
            self._last._next = ptr
            ptr._prev = self._last
            self._last = ptr
            

    def pop(self):
        if linked_list.is_Empty(self) == False :
            popped = self._last
            new_last = self._last._prev
            if self._head != self._last :
                new_last._next = None
                self._last = new_last
            else :
                self._head = None
                self._last = None
        
            return popped._capacity

# heap_index is another list which stores the address of the elements in the same order as that of the heap i.e the 0th index of heap_index refers to the minimum(or root) element of the heap and so on .
def swap(heap_index,x1,x2):   # swap the addresses and update the m of their nodes to their new value.
    u_initial = heap_index[x1]
    x2_val = heap_index[x2]
    heap_index[x1] = x2_val 
    heap_index[x2] = u_initial
    heap_index[x2]._m = x2
    heap_index[x1]._m = x1
    m = x2  

def Heap_up(vertex_num,Address_list,heap_index):  # Performs heap up operation.
    m = Address_list[vertex_num]._m
    u = heap_index[m]
    while ((u._capacity > heap_index[(m-1)//2]._capacity) or (u._capacity == heap_index[(m-1)//2]._capacity and u._vertex_num < heap_index[(m-1)//2]._vertex_num)):
        a = m
        b = (m-1)//2
        swap(heap_index,a,b) 
        m = b
        u = heap_index[b]
        if m < 1:
            break

def Heap_Down(vertex_num,Address_list,heap_index):  # Performs heap down operation .
    m = Address_list[vertex_num]._m
    u = heap_index[m]
    child_1 = 2*m+1
    child_2 = 2*m+2

    if child_1 <= len(heap_index)-1 :
        if child_1 == len(heap_index)-1:   # if the last parent has only one child then take its another child(right child)  = left child .
            child_2 = child_1

        while ((u._capacity < heap_index[child_1]._capacity) or (u._capacity < heap_index[child_2]._capacity) or (u._capacity == heap_index[child_1]._capacity and u._vertex_num > heap_index[child_1]._vertex_num) or (u._capacity == heap_index[child_2]._capacity and u._vertex_num > heap_index[child_2]._vertex_num)) :   # condition impose on equality or loop termination
            max = heap_index[child_1]
            if heap_index[child_1]._capacity < heap_index[child_2]._capacity :
                max = heap_index[child_2]
            elif heap_index[child_1]._capacity == heap_index[child_2]._capacity :
                if heap_index[child_1]._vertex_num > heap_index[child_2]._vertex_num:
                    max = heap_index[child_2]

            a = max._m
            b = m
            
            swap(heap_index,a,b)
            m = a  
            u = heap_index[a]
            child_1 = 2*m+1
            child_2 = 2*m+2

            if 2*m + 1 > len(heap_index)-1 : # if we reached at mth index which does not have any child then break.
                break
            elif 2*m+1 == len(heap_index)-1:
                child_2 = child_1

def enqueue(vertex_num,capacity,heap_index,Address_list,heap):   # enqueue a new element in the heap.
    heap.push(vertex_num,capacity,len(heap_index),True)
    enqueued_element = Address_list[-1]
    heap_index.append(enqueued_element)
    Address_list[vertex_num] = enqueued_element
    Address_list.pop(-1)
    Heap_up(vertex_num,Address_list,heap_index)

def extract_max(heap,Address_list,heap_index):  # extracting the root from heap and updating the address list as -1 which indicates that it is not present in the heap.
    if len(heap_index) > 0: 
        vertex_num_of_max = heap_index[0]._vertex_num
        dequeued = heap_index[0]
        swap(heap_index,0,len(heap_index)-1)
        heap.pop()
        heap_index.pop(-1)
        Address_list[vertex_num_of_max] = -1
        if len(heap_index) > 0:
            Heap_Down(heap_index[0]._vertex_num,Address_list,heap_index)
        return dequeued

def findMaxCapacity(n,links,s,t):
    route_list = [] # the path which needs to be returned 
    heap = linked_list(n,True) 
    heap_index = [] # heap_index is another list which stores the address of the elements in the same order as that of the heap i.e the 0th index of heap_index refers to the minimum(or root) element of the heap and so on .
    vertex_arr = [] # an array whose each element will store a list of 3 elements (a list which contains the neighbour of the vertex, the maximum capacity of that node from the source,the previous vertex_num whose dequeue operation let this vertex being enqueued or modified inside the heap) as its element.
    cap_current = -1

    for i in range (n): 
        vertex_arr.append([[],cap_current,None])

    for j in range (len(links)):  # creating graph using adjacency lists.
        capacity = links[j][2]
        first_vetex = links[j][0]
        second_vertex = links[j][1]
        vertex_arr[first_vetex][0].append((second_vertex,capacity))
        vertex_arr[second_vertex][0].append((first_vetex,capacity))
    vertex_arr[s][1] = 0   # made the capacity of the source 0.

    k = 0
    while k < len(vertex_arr[s][0]) :  # enqueued all the neighbours of s and if it had multiple links between s and its neighbour and firstly if link with less capacity was enqueued and then a link with greater capacity is encountered between the source and its neighbour , update its capacity in the vertex_arr as well inside the heap.
        s_neighbour = vertex_arr[s][0][k][0]
        s_neighbour_capacity = vertex_arr[s][0][k][1]
        vertex_arr[s_neighbour][2] = s
        if heap._l[s_neighbour] == -1: 
            vertex_arr[s_neighbour][1] = s_neighbour_capacity
            enqueue(s_neighbour,vertex_arr[s_neighbour][1],heap_index,heap._l,heap)
        else:
            if vertex_arr[s_neighbour][1] < s_neighbour_capacity:
                vertex_arr[s_neighbour][1] = s_neighbour_capacity
                heap._l[s_neighbour]._capacity = s_neighbour_capacity
            
            if heap._l[s_neighbour]._m >= 1 : 
                if (heap_index[(heap._l[s_neighbour]._m-1)//2]._capacity >= s_neighbour_capacity):
                    Heap_Down(s_neighbour,heap._l,heap_index)
                elif (heap_index[(heap._l[s_neighbour]._m-1)//2]._capacity <= s_neighbour_capacity):
                    Heap_up(s_neighbour,heap._l,heap_index)
            else:
                Heap_Down(s_neighbour,heap._l,heap_index)
        
        k += 1

    while heap._head != None:  # loop will run until capacity of every element is updated (every elements's capacity is updated since it a connected graph)
        
        x = extract_max(heap,heap._l,heap_index)
        l = 0
        while l < len(vertex_arr[x._vertex_num][0]): # enqueing all the neighbours of x and updating their capacity if needed and if already present in the heap updating their capacities in the vertex_arr's elements' cap_current and also updating their capacities in the heap and adjusting the heap accordingly.
            x_neighbour = vertex_arr[x._vertex_num][0][l][0]
            x_neighbour_capacity = vertex_arr[x._vertex_num][0][l][1]
            if x_neighbour != vertex_arr[x._vertex_num][2] and x_neighbour != s :
                
                minimum = vertex_arr[x._vertex_num][1]
                if minimum > x_neighbour_capacity :
                    minimum = x_neighbour_capacity

                if minimum > vertex_arr[x_neighbour][1] :
                    vertex_arr[x_neighbour][1] = minimum  
                    vertex_arr[x_neighbour][2] = x._vertex_num
                    if heap._l[x_neighbour] == -1: 
                        enqueue(x_neighbour,vertex_arr[x_neighbour][1],heap_index,heap._l,heap)
                    else:
                        heap._l[x_neighbour]._capacity = minimum
                       
                        if heap._l[x_neighbour]._m >= 1 : 
                            if (heap_index[(heap._l[x_neighbour]._m-1)//2]._capacity >= minimum):
                                Heap_Down(x_neighbour,heap._l,heap_index)
                            elif (heap_index[(heap._l[x_neighbour]._m-1)//2]._capacity <= minimum):
                                Heap_up(x_neighbour,heap._l,heap_index)
                        else:
                            Heap_Down(x_neighbour,heap._l,heap_index)

            l += 1

    router_num = t # tracing back the path from the target to the source .
    route_list.append(router_num)
    while router_num != s:
        route_list.append(vertex_arr[router_num][2])
        router_num = vertex_arr[router_num][2]
        
    for m in range (len(route_list)//2):  # reversing the list to obtain the path from source to target . 
        swap = route_list[m]
        route_list[m] = route_list[-1-m]
        route_list[-1-m] = swap
   
    return (vertex_arr[t][1],route_list)




