# Classe Graph para representação de Grafos
import math
from queue import Queue

import networkx as nx            # biblioteca de tratamento de grafos necessária para desnhar graficamente o grafo
import matplotlib.pyplot as plt  # idem


from Node import Node

class Grafo:

    def __init__(self, directed=False):
        self.m_nodes = []
        self.m_directed = directed
        self.m_graph = {}               # dicionario para armazenar os nodos e arestas
        self.m_h = {}                   # dicionario para posteriormente armazenar as heuristicas para cada nodo -> pesquisa informada
        self.nestedCircuito = None

    # Escrever o grafo como String
    def __str__(self):
        out = ""
        for key in self.m_graph.keys():
            out = out + "node" + str(key) + ": " + str(self.m_graph[key]) + "\n"
        return out

    # Encontrar nodo pelo nome
    def get_node_by_name(self, name):
        search_node = Node(name)
        for node in self.m_nodes:
            if node == search_node:
                return node
            else:
                return None

    # Imprimir arestas
    def imprime_aresta(self):
        listaA = ""
        lista = self.m_graph.keys()
        for nodo in lista:
            for (nodo2, custo) in self.m_graph[nodo]:
                listaA = listaA + nodo + " ->" + nodo2 + "\n" # + " custo:" + str(custo) + "\n"
        return listaA

    # Adicionar   aresta no grafo
    def add_edge(self, node1, node2, weight):
        n1 = Node(node1)
        n2 = Node(node2)
        if (n1 not in self.m_nodes):
            self.m_nodes.append(n1)
            self.m_graph[node1] = list()
        else:
            n1 = self.get_node_by_name(node1)

        if (n2 not in self.m_nodes):
            self.m_nodes.append(n2)
            self.m_graph[node2] = list()
        else:
            n2 = self.get_node_by_name(node2)

        self.m_graph[node1].append((node2, weight))


        if not self.m_directed:
            self.m_graph[node2].append((node1, weight))

    # Devolver nodos do Grafo
    def getNodes(self):
        return self.m_nodes
    # Devolver o custo de uma aresta
    def get_arc_cost(self, node1, node2):
        custoT = math.inf
        a = self.m_graph[node1]  # lista de arestas para aquele nodo
        nodeInA = [item for item in a if item[0] == node2]
        if len(nodeInA) == 0:
            custoT = 1
        else:
            for (nodo, custo) in a:
                if nodo == node2:
                    custoT = custo

        return custoT

    # Algoritmo de Procura DFS
    def procura_DFS(self, start, end, path=None, visited=None):
        if path == None:
            path = []
        if visited == None:
            visited = set()

        path.append(start)
        visited.add(start)

        if start == end:
            # calcular o custo do caminho funçao calcula custo.
            custoT = self.calcula_custo(path)
            return (path, custoT)
        for (adjacente, peso) in self.m_graph[start]:
            # print(f"adjacentes : {adjacente}\visited : {visited}")
            if peso!=25 and adjacente not in visited:
                resultado = self.procura_DFS(adjacente, end, path, visited)
                if resultado is not None:
                    return resultado
        path.pop()  # se nao encontra remover o que está no caminho......
        return None

    # Algoritmo de Procura BFS
    def procura_BFS(self, start, end):
        # definir nodos visitados para evitar ciclos
        visited = set()
        fila = Queue()

        # adicionar o nodo inicial à fila e aos visitados
        fila.put(start)
        visited.add(start)

        # garantir que o start node nao tem pais...
        parent = dict()
        parent[start] = None

        path_found = False
        while not fila.empty() and path_found == False:
            nodo_atual = fila.get()
            if nodo_atual == end:
                path_found = True
            else:
                for (adjacente, peso) in self.m_graph[nodo_atual]:
                    if peso!=25 and adjacente not in visited:
                        fila.put(adjacente)
                        parent[adjacente] = nodo_atual
                        visited.add(adjacente)



        # Reconstruir o caminho

        path = []
        if path_found:
            path.append(end)
            while parent[end] is not None:
                path.append(parent[end])
                end = parent[end]
            path.reverse()
            # funçao calcula custo caminho
            custo = self.calcula_custo(path)
        return (path, custo)


    # Desenha grafo em modo grafico
    def desenha(self):
        ##criar lista de vertices
        lista_v = self.m_nodes
        lista_a = []
        g = nx.Graph()
        for nodo in lista_v:
            n = nodo.getName()
            g.add_node(n)
            for (adjacente, peso) in self.m_graph[n]:
                lista = (n, adjacente)
                # lista_a.append(lista)
                g.add_edge(n, adjacente, weight=peso)

        pos = nx.spring_layout(g)
        nx.draw_networkx(g, pos, with_labels=True, font_weight='bold')
        labels = nx.get_edge_attributes(g, 'weight')
        nx.draw_networkx_edge_labels(g, pos, edge_labels=labels)

        plt.draw()
        plt.show()

    #  Define heuristica para cada nodo
    def add_heuristica(self, n, estima):
        n1 = Node(n)
        if n1 in self.m_nodes:
            self.m_h[n] = estima

    # Heuristica -> define heuristica para cada nodo 1 por defeito
    # Nota -> apenas para teste de pesquisa informada
    def heuristica(self):
        nodos = self.m_graph.keys()
        for s in nodos:
            print(s)
            # self.m_h[n] = 1
        return (True)

    def getDistance(self, i, f):
        x, y = i
        xf, yf = f
        dx = abs(x - xf)
        dy = abs(y - yf)
        return 1 * (dx + dy) - min(dx, dy) # D * (dx + dy) + (D2 - 2 * D) * min(dx, dy)
    
    ##########################################


    def PStrTuple(self, pontoString):
        res = pontoString[1:-1]
        res = res.split(',')
        resint = list(map(int, res))
        tup = (resint[0], resint[1])
        return tup

    def heuristica_aStar(self, nFinal):
        nodos = self.m_graph.keys()
        for n in nodos:
            if n == nFinal:
                self.m_h[n] = 0
            else: self.m_h[n] = self.getDistance(self.PStrTuple(n), self.PStrTuple(nFinal)) + 1
        return (True)

    def calcula_custo(self, caminho):
        # caminho é uma lista de nodos
        teste = caminho
        custo = 0
        i = 0
        while i + 1 < len(teste):
            custo = custo + self.get_arc_cost(teste[i], teste[i + 1])
            #print(teste[i])
            i = i + 1
        return custo

    def calcula_est(self, estima):
        l = list(estima.keys())
        min_estima = estima[l[0]]
        node = l[0]
        for k, v in estima.items():
            if v < min_estima:
                min_estima = v
                node = k
            # elif v == min_estima:
                # if self.m_h[node] > self.m_h[k]:
                    # min_estima = v
                    # node = k
        return node
        
    # Devolve heuristica do nodo
    def getH(self, nodo):
        if nodo not in self.m_h.keys():
            return 1000
        else:
            return (self.m_h[nodo])

    def add_circuito(self, nestedCircuitoooo):
        self.nestedCircuito = nestedCircuitoooo
        


    def PStringtoArr(self, pontoString):
        res = pontoString[1:-1]
        res = res.split(',')
        resint = list(map(int, res))
        return resint

    def barreirasBetween(self, p1x, p1y, p2x, p2y):
        tabuleiro = self.nestedCircuito
        # Check for trivial cases
        if p1x == p2x and p1y == p2y:
            return True
        if p1x == p2x:
            miny = min(p1y, p2y)
            maxy = max(p1y, p2y)
            for y in range(miny, maxy+1):
                if tabuleiro[p1x][y] == 'X':
                    return False
            return True
        if p1y == p2y:
            minx = min(p1x, p2x)
            maxx = max(p1x, p2x)
            for x in range(minx, maxx+1):
                if tabuleiro[x][p1y] == 'X':
                    return False
            return True

        # Use Bresenham's line algorithm to draw a line between the two points
        dx = abs(p2x - p1x)
        dy = abs(p2y - p1y)
        sx = 1 if p1x < p2x else -1
        sy = 1 if p1y < p2y else -1
        err = dx - dy
        while True:
            if tabuleiro[p1x][p1y] == 'X':
                return False
            if p1x == p2x and p1y == p2y:
                break
            e2 = err * 2
            if e2 > -dy:
                err -= dy
                p1x += sx
            if e2 < dx:
                err += dx
                p1y += sy
        return True

    def ArrToVString(self, velArr):
        res = "(" + str(velArr[0]) + "," + str(velArr[1]) + ")"
        return res

     # Função que devolve vizinhos de um nó
    # def getNeighboursVel(self, nodo, vel):
        # lista = []
        # x = self.PStringtoArr(nodo)
        # xV, yV = vel
        # velocidades = []
# 
        # if xV < 0 and yV < 0: 
            # for x in range(xV-1, 0):
                # for y in range(yV-1, 0):
                    # velocidades.append([x,y])
        # elif xV > 0 and yV > 0:
            # for x in range(0, xV+2):
                # for y in range(0, yV+2):
                    # velocidades.append([x,y])
        # elif xV < 0 and yV > 0:
            # for x in range(xV-1, 0):
                # for y in range(0, yV+2):
                    # velocidades.append([x,y])
        # elif xV > 0 and yV < 0:
            # for x in range(0, xV+2):
                # for y in range(yV-1, 0):
                    # velocidades.append([x,y])
        # elif xV == 0 and yV == 0:
            # for x in range(-1, 2):
                # for y in range(-1, 2):
                    # velocidades.append([x,y])
        # elif xV == 0 and yV < 0:
            # for x in range(-1, 2):
                # for y in range(yV-1, 0):
                    # velocidades.append([x,y])
        # elif xV == 0 and yV > 0:
            # for x in range(-1, 2):
                # for y in range(0, yV+2):
                    # velocidades.append([x,y])
        # elif xV < 0 and yV == 0:
            # for x in range(xV-1, 0):
                # for y in range(-1, 1):
                    # velocidades.append([x,y])
        # elif xV > 0 and yV == 0:
            # for x in range(0, xV+2):
                # for y in range(-1, 1):
                    # velocidades.append([x,y])
# 
        # for idx, x in enumerate(velocidades):
            # if x == [0,0]:
                # velocidades.pop(idx)
# 
        # listaPsArr = []
        # for v in velocidades:
            # listaPsArr.append([int(x[0])+v[0],int(x[1])+v[1]])
        # 
        # listaPs = []
        # for p in listaPsArr:
            # listaPs.append(self.ArrToVString(p))
# 
        # for p in listaPs:
            # ret = False
            # if p in self.m_graph:
                # golo = self.PStringtoArr(p)
                # if self.barreirasBetween(x[0], x[1], golo[0], golo[1]):
                    # for adjs in self.m_graph[nodo]:
                        # adj, peso = adjs
                        # if adj == p:
                            # lista.append((adj, peso))
                            # ret = True
                            # break
                    # if not ret:
                        # lista.append((p, 1))
                        # 
        # return lista

     # Função que devolve vizinhos de um nó
    def getNeighboursVel(self, nodo, vel):
        lista = []
        x = self.PStringtoArr(nodo)
        for xx in range(x[0], x[0]+vel):
            for yy in range(x[1], x[1]+vel):
                if f'({xx},{yy})' in self.m_graph:
                        for (adjacente, peso) in self.m_graph[f'({xx},{yy})']:
                            # if peso!=25:
                            if self.barreirasBetween(x[0], x[1], xx, yy):
                                lista.append((adjacente, peso))
        return lista

# Algoritmo A*
    def procura_aStar_wVelocity(self, start, end):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        closed_list_a = set([])
        open_list = {start}

        # velocidade = (0,0)
        velocidade = 1

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[start] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start
        n = None
        while len(open_list) > 0:
            # find a node with the lowest value of f() - evaluation function
            calc_heurist = {}
            flag = 0
            for v in open_list:
                if n == None:
                    n = v
                else: 
                    flag = 1
                    calc_heurist[v] = (g[v] + self.getH(v))#/velocidade
            if flag == 1:
                min_estima = self.calcula_est(calc_heurist)
                n = min_estima
            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                #print('Path found: {}'.format(reconst_path))
                return (reconst_path, self.calcula_custo(reconst_path))

            # for all neighbors of the current node do
            for (m, weight) in self.getNeighboursVel(n, velocidade):  # definir função getneighbours  tem de ter um par nodo peso
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list_a:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list_a:
                            closed_list_a.remove(m)
                            open_list.add(m)
            # velocidade = tuple(map(lambda i, j: i + j, velocidade, (1,1)))
            velocidade += 1

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list_a.add(n)

        print('Path does not exist!')
        return None

    # Função que devolve vizinhos de um nó
    def getNeighbours(self, nodo):
        lista = []
        for (adjacente, peso) in self.m_graph[nodo]:
            lista.append((adjacente, peso))
        return lista

    # Algoritmo A*
    def procura_aStar(self, start, end):
        # open_list is a list of nodes which have been visited, but who's neighbors
        # haven't all been inspected, starts off with the start node
        # closed_list is a list of nodes which have been visited
        # and who's neighbors have been inspected
        closed_list_a = set([])
        open_list = {start}

        # g contains current distances from start_node to all other nodes
        # the default value (if it's not found in the map) is +infinity
        g = {}

        g[start] = 0

        # parents contains an adjacency map of all nodes
        parents = {}
        parents[start] = start
        n = None
        while len(open_list) > 0:
            # find a node with the lowest value of f() - evaluation function
            calc_heurist = {}
            flag = 0
            for v in open_list:
                if n == None:
                    n = v
                else:
                    flag = 1
                    calc_heurist[v] = g[v] + self.getH(v) * (1 + 1/1000)
            if flag == 1:
                min_estima = self.calcula_est(calc_heurist)
                n = min_estima
            if n == None:
                print('Path does not exist!')
                return None

            # if the current node is the stop_node
            # then we begin reconstructin the path from it to the start_node
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                #print('Path found: {}'.format(reconst_path))
                return (reconst_path, self.calcula_custo(reconst_path))

            # for all neighbors of the current node do
            for (m, weight) in self.getNeighbours(n):  # definir função getneighbours  tem de ter um par nodo peso
                # if the current node isn't in both open_list and closed_list
                # add it to open_list and note n as it's parent
                if m not in open_list and m not in closed_list_a:
                    open_list.add(m)
                    parents[m] = n
                    g[m] = g[n] + weight

                # otherwise, check if it's quicker to first visit n, then m
                # and if it is, update parent data and g data
                # and if the node was in the closed_list, move it to open_list
                else:
                    if g[m] > g[n] + weight:
                        g[m] = g[n] + weight
                        parents[m] = n

                        if m in closed_list_a:
                            closed_list_a.remove(m)
                            open_list.add(m)

            # remove n from the open_list, and add it to closed_list
            # because all of his neighbors were inspected
            open_list.remove(n)
            closed_list_a.add(n)

        print('Path does not exist!')
        return None



    def heuristica_greedy(self, nFinal):
        nodos = self.m_graph.keys()
        for n in nodos:
            if n == nFinal:
                self.m_h[n] = 0
            else: self.m_h[n] = self.getDistance(self.PStrTuple(n), self.PStrTuple(nFinal))
        return (True)

    # def shortenClosedListToCollision_a(self, collisionPoint):
        # global closed_list_a
        # tempList = list(closed_list_a)
        # pointIndex = tempList.index(collisionPoint)
        # closed_list_a = set(tempList[:pointIndex])

    # def shortenClosedListToCollision_greedy(self, collisionPoint):
        # global closed_list_greedy
        # tempList = list(closed_list_greedy)
        # pointIndex = tempList.index(collisionPoint)
        # closed_list_greedy = set(tempList[:pointIndex])

    # Algoritmo Greedy
    def greedy(self, start, end):
        # open_list é uma lista de nodos visitados, mas com vizinhos
        # que ainda não foram todos visitados, começa com o  start
        # closed_list é uma lista de nodos visitados
        # e todos os seus vizinhos também já o foram
        closed_list_greedy = set([])
        open_list = set([start])

        # parents é um dicionário que mantém o antecessor de um nodo
        # começa com start
        parents = {}
        parents[start] = start

        while len(open_list) > 0:
            n = None

            # encontraf nodo com a menor heuristica
            for v in open_list:
                if n == None or self.m_h[v] < self.m_h[n]:
                    n = v

            if n == None:
                print('Path does not exist!')
                return None

            # se o nodo corrente é o destino
            # reconstruir o caminho a partir desse nodo até ao start
            # seguindo o antecessor
            if n == end:
                reconst_path = []

                while parents[n] != n:
                    reconst_path.append(n)
                    n = parents[n]

                reconst_path.append(start)

                reconst_path.reverse()

                return (reconst_path, self.calcula_custo(reconst_path))

            # para todos os vizinhos  do nodo corrente
            for (m, weight) in self.getNeighbours(n):
                # Se o nodo corrente nao esta na open nem na closed list
                # adiciona-lo à open_list e marcar o antecessor
                if weight!=25 and m not in open_list and m not in closed_list_greedy:
                    open_list.add(m)
                    parents[m] = n

            # remover n da open_list e adiciona-lo à closed_list
            # porque todos os seus vizinhos foram inspecionados
            open_list.remove(n)
            closed_list_greedy.add(n)

        print('Path does not exist!')
        return None
