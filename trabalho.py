import networkx as nx
import matplotlib.pyplot as plt
from collections import defaultdict
from time import sleep

class Grafo:
    def __init__(self):
        self.vertices = set()
        self.arestas = defaultdict(list)

    def adicionar_aresta(self, vertice_origem, vertice_destino):
        self.vertices.add(vertice_origem)
        self.vertices.add(vertice_destino)
        self.arestas[vertice_origem].append(vertice_destino)

    def obter_grau_saida(self, vertice):
        return len(self.arestas[vertice])

    def obter_vertices_ordenados_por_grau_saida(self):
        return sorted(self.vertices, key=self.obter_grau_saida, reverse=True)

    def dfs(self):
        vertices = self.obter_vertices_ordenados_por_grau_saida()

        for vertice_inicio in vertices:
            visitados = set()
            d = {}
            f = {}
            tempo = [0]  # Tempo será uma lista para manter a referência entre as chamadas recursivas
            tipos_aresta = {}
            cores_vertices = {}

            print(f"Executando DFS a partir do vértice {vertice_inicio}")

            self._dfs_visit_tipos_aresta(vertice_inicio, visitados, d, f, tempo, tipos_aresta, cores_vertices)
            sleep(5)

            self.imprimir_resultados(d, f, tipos_aresta)

            sleep(5)
            print("Deseja visualizar o grafo? (s/n)")
            opcao = input()
            if opcao == "s":
                self.visualizar_grafo(tipos_aresta, cores_vertices)
            else:
                print("Ok, até a próxima!")
            break

    def _dfs_visit_tipos_aresta(self, vertice, visitados, d, f, tempo, tipos_aresta, cores_vertices):
        visitados.add(vertice)
        d[vertice] = tempo[0]
        tempo[0] += 1
        cores_vertices[vertice] = 'gray'  # Define a cor do vértice como cinza

        for vizinho in self.arestas.get(vertice, []):
            if vizinho not in visitados:
                tipos_aresta[(vertice, vizinho)] = "Aresta de Árvore"
                self._dfs_visit_tipos_aresta(vizinho, visitados, d, f, tempo, tipos_aresta, cores_vertices)
            elif f.get(vizinho) is None:
                tipos_aresta[(vertice, vizinho)] = "Aresta de Retorno"
            elif d[vertice] < d[vizinho]:
                tipos_aresta[(vertice, vizinho)] = "Aresta de Avanço"
            else:
                tipos_aresta[(vertice, vizinho)] = "Aresta de Cruzamento"

        f[vertice] = tempo[0]
        tempo[0] += 1
        cores_vertices[vertice] = 'black'  # Define a cor do vértice como preto

    def imprimir_resultados(self, d, f, tipos_aresta):
        sleep(1)
        print("Vertices Visitados:")
        for vertice, tempo in d.items():
            print(vertice, ": d =", tempo, ", f =", f[vertice])
        print("-------------------")
        print()

        print("-------------------")
        print("Tipo de aresta:")
        for (vertice_origem, vertice_destino), tipo in tipos_aresta.items():
            print(vertice_origem, "->", vertice_destino, ":", tipo)
        print("-------------------")

    def visualizar_grafo(self, tipos_aresta, cores_vertices):
        sleep(1)
        G = nx.DiGraph()
        for vertice in self.vertices:
            G.add_node(vertice)

        for vertice_origem, vertices_destino in self.arestas.items():
            for vertice_destino in vertices_destino:
                G.add_edge(vertice_origem, vertice_destino)

        pos = nx.spring_layout(G) # type: ignore
        plt.figure(figsize=(10, 6))

        # Define as cores dos vértices
        cores = ['white'] * len(G.nodes())

        # Define a cor de fundo do grafo
        plt.gca().set_facecolor('lightgray')

        nx.draw_networkx(G, pos, with_labels=True, node_color=cores, node_size=800, font_size=12, font_color='black') # type: ignore

        cores_aresta = {
            "Aresta de Árvore": "green",
            "Aresta de Retorno": "red",
            "Aresta de Avanço": "blue",
            "Aresta de Cruzamento": "orange"
        }

        for (vertice_origem, vertice_destino), tipo in tipos_aresta.items():
            cor_aresta = cores_aresta.get(tipo)
            nx.draw_networkx_edges(G, pos, edgelist=[(vertice_origem, vertice_destino)], # type: ignore
                                   edge_color=cor_aresta, arrows=True)

            nx.draw_networkx_edge_labels(G, pos, edge_labels={(vertice_origem, vertice_destino): tipo}, # type: ignore
                                         label_pos=0.5, font_color='black', font_size=8, verticalalignment='bottom')

            plt.pause(1)
            plt.draw()

        plt.show()

def carregar_grafo(nome_arquivo):
    grafo = Grafo()
    with open(nome_arquivo, 'r') as arquivo:
        for linha in arquivo:
            if not linha.startswith('d'):
                origem, destino = linha.split()
                grafo.adicionar_aresta(origem, destino)
    return grafo

# Exemplo de uso:
nome_arquivo = "Grafos.txt"  # substitua pelo nome do arquivo de texto com as informações do grafo
grafo = carregar_grafo(nome_arquivo)
grafo.dfs()
