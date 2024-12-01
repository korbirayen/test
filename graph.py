from collections import defaultdict, deque
import heapq

class Graphe:
    def __init__(self):
        self.type_graphe = None  # 'orienté' ou 'non orienté'
        self.representation_graphe = None  # 'adjacence', 'incidence', ou 'dictionnaire'
        self.matrice_adjacence = []
        self.matrice_incidence = []
        self.n = 0

    def acquérir_graphe(self):
        print("Entrez le type de graphe (orienté/non orienté) :")
        self.type_graphe = input().strip().lower()
        print("Entrez la méthode d'entrée (adjacence/incidence/dictionnaire) :")
        self.representation_graphe = input().strip().lower()

        if self.representation_graphe == 'adjacence':
            self._entrer_matrice_adjacence()
        elif self.representation_graphe == 'incidence':
            self._entrer_matrice_incidence()
        elif self.representation_graphe == 'dictionnaire':
            self._entrer_dictionnaire()
        else:
            print("Méthode d'entrée invalide.")

    def _entrer_matrice_adjacence(self):
        print("Entrez le nombre de sommets :")
        self.n = int(input().strip())
        print("Entrez la matrice d'adjacence ligne par ligne :")
        self.matrice_adjacence = [list(map(int, input().strip().split())) for _ in range(self.n)]

    def _entrer_matrice_incidence(self):
        print("Entrez le nombre de sommets :")
        self.n = int(input().strip())
        print("Entrez la matrice d'incidence ligne par ligne :")
        print("Note : Les colonnes représentent les arêtes, les lignes représentent les sommets.")
        self.matrice_incidence = [list(map(int, input().strip().split())) for _ in range(self.n)]
        self.matrice_adjacence = [[0] * self.n for _ in range(self.n)]

        for j in range(len(self.matrice_incidence[0])):  # Itérer sur les arêtes
            sommets = [i for i in range(self.n) if self.matrice_incidence[i][j] != 0]
            if len(sommets) == 2:
                u, v = sommets
                self.matrice_adjacence[u][v] = self.matrice_incidence[u][j]
                if self.type_graphe == "non orienté":
                    self.matrice_adjacence[v][u] = self.matrice_incidence[v][j]

    def _entrer_dictionnaire(self):
        print("Entrez le nombre de sommets :")
        self.n = int(input().strip())
        self.matrice_adjacence = [[0] * self.n for _ in range(self.n)]
        print("Entrez le dictionnaire des voisins (clé : liste de voisins) :")

        for _ in range(self.n):
            sommet, voisins = input("Sommet et voisins (ex : 1: 2,3) : ").split(':')
            sommet = int(sommet.strip()) - 1
            voisins = voisins.strip()

            # Si pas de voisins, sauter la conversion
            if voisins:
                voisins = list(map(int, voisins.strip().split(',')))
            else:
                voisins = []

            for voisin in voisins:
                voisin = voisin - 1
                self.matrice_adjacence[sommet][voisin] = 1
                if self.type_graphe == "non orienté":
                    self.matrice_adjacence[voisin][sommet] = 1

    def afficher_graphe(self):
        print("Type de graphe :", self.type_graphe)
        print("Matrice d'adjacence :")
        for ligne in self.matrice_adjacence:
            print(ligne)

    # Tâche 1 : Vérifier la connectivité (Graphe Non Orienté)
    def est_connexe(self):
        visites = set()
        self._dfs(0, visites)
        return len(visites) == self.n

    def _dfs(self, noeud, visites):
        visites.add(noeud)
        for voisin, connecte in enumerate(self.matrice_adjacence[noeud]):
            if connecte and voisin not in visites:
                self._dfs(voisin, visites)

    # Tâche 2 : Algorithme de Prim pour l'Arbre Couvrant Maximal (Graphe Non Orienté)
    def arbre_couvrant_maximal_prim(self):
        visites = [False] * self.n
        visites[0] = True  # Commencer du sommet 0
        poids_max = 0

        while True:
            arête_max = None
            poids_arête_max = -1

            # Trouver l'arête de poids maximum connectant les sommets visités aux sommets non visités
            for u in range(self.n):
                if visites[u]:
                    for v in range(self.n):
                        if not visites[v] and self.matrice_adjacence[u][v] > 0:
                            if self.matrice_adjacence[u][v] > poids_arête_max:
                                poids_arête_max = self.matrice_adjacence[u][v]
                                arête_max = (u, v)

            if arête_max is None:  # Plus d'arêtes à ajouter, terminé
                break
            
            # Ajouter l'arête sélectionnée à l'AGM
            u, v = arête_max
            visites[v] = True  # Marquer le sommet v comme visité
            poids_max += self.matrice_adjacence[u][v]  # Ajouter son poids au poids total de l'AGM

        return poids_max

    # Tâche 3 : Algorithme de Kruskal pour l'Arbre Couvrant Minimal (Graphe Non Orienté)
    def arbre_couvrant_minimal_kruskal(self):
        arêtes = []
        for i in range(self.n):
            for j in range(i + 1, self.n):
                if self.matrice_adjacence[i][j] > 0:
                    arêtes.append((self.matrice_adjacence[i][j], i, j))
        arêtes.sort()
        parent = list(range(self.n))

        def trouver(x):
            if parent[x] != x:
                parent[x] = trouver(parent[x])
            return parent[x]

        def union(x, y):
            parent[trouver(x)] = trouver(y)

        poids_acm = 0
        for poids, u, v in arêtes:
            if trouver(u) != trouver(v):
                union(u, v)
                poids_acm += poids
        return poids_acm

    # Tâche 4 : Connexité Forte (Graphe Orienté)
    def est_fortement_connexe(self):
        def bfs(départ, graphe):
            visites = set()
            file = deque([départ])
            while file:
                noeud = file.popleft()
                visites.add(noeud)
                for voisin, connecte in enumerate(graphe[noeud]):
                    if connecte and voisin not in visites:
                        file.append(voisin)
            return visites

        # BFS pour le graphe original
        visites = bfs(0, self.matrice_adjacence)
        if len(visites) != self.n:
            return False

        # BFS pour le graphe transposé
        transposé = [[self.matrice_adjacence[j][i] for j in range(self.n)] for i in range(self.n)]
        visites_transposé = bfs(0, transposé)
        return len(visites_transposé) == self.n

    # Tâche 5 : Fournir le Graphe Réduit
    def graphe_reduit(self):
        if self.est_fortement_connexe():
            print("Le graphe est déjà fortement connexe.")
        else:
            print("Graphe réduit :")
            print(self._reduire_graphe())

    def _reduire_graphe(self):
        # Trouver les composantes fortement connexes avec l'algorithme de Kosaraju
        def dfs(noeud, visites, pile, graphe):
            visites.add(noeud)
            for voisin, connecte in enumerate(graphe[noeud]):
                if connecte and voisin not in visites:
                    dfs(voisin, visites, pile, graphe)
            pile.append(noeud)

        pile = []
        visites = set()
        for i in range(self.n):
            if i not in visites:
                dfs(i, visites, pile, self.matrice_adjacence)

        transposé = [[self.matrice_adjacence[j][i] for j in range(self.n)] for i in range(self.n)]
        visites.clear()
        composantes = []
        while pile:
            noeud = pile.pop()
            if noeud not in visites:
                composante = []
                dfs(noeud, visites, composante, transposé)
                composantes.append(composante)
        return composantes

    # Tâche 6 : Détection du Sommet Racine
    def sommet_racine(self):
        racines = [all(ligne) for ligne in zip(*self.matrice_adjacence)]
        if sum(racines) == 1:
            return racines.index(True)
        return None

    # Tâche 7 : Chemin le Plus Long avec Choix d'Algorithme
    def chemin_le_plus_long(self, racine, algorithme="bellman-ford"):
        if algorithme == "bellman-ford":
            return self._chemin_le_plus_long_bellman_ford(racine)
        elif algorithme == "dijkstra":
            return self._chemin_le_plus_long_dijkstra(racine)

    def _chemin_le_plus_long_bellman_ford(self, racine):
        distance = [-float('inf')] * self.n
        distance[racine] = 0
        for _ in range(self.n - 1):
            for u in range(self.n):
                for v in range(self.n):
                    if self.matrice_adjacence[u][v] > 0:
                        distance[v] = max(distance[v], distance[u] + self.matrice_adjacence[u][v])
        return distance

    def _chemin_le_plus_long_dijkstra(self, racine):
        distance = [-float('inf')] * self.n
        distance[racine] = 0
        file = [(-0, racine)]
        while file:
            dist, noeud = heapq.heappop(file)
            for voisin in range(self.n):
                if self.matrice_adjacence[noeud][voisin] > 0:
                    nouvelle_dist = -dist + self.matrice_adjacence[noeud][voisin]
                    if nouvelle_dist > distance[voisin]:
                        distance[voisin] = nouvelle_dist
                        heapq.heappush(file, (-nouvelle_dist, voisin))
        return distance

# Fonction Principale
if __name__ == "__main__":
    graphe = Graphe()
    graphe.acquérir_graphe()
    graphe.afficher_graphe()

    if graphe.type_graphe == "non orienté":
        print("Le graphe est-il connexe ?", graphe.est_connexe())
        print("Poids de l'Arbre Couvrant Maximal (Prim) :", graphe.arbre_couvrant_maximal_prim())
        print("Poids de l'Arbre Couvrant Minimal (Kruskal) :", graphe.arbre_couvrant_minimal_kruskal())
    elif graphe.type_graphe == "orienté":
        print("Le graphe est-il fortement connexe ?", graphe.est_fortement_connexe())
        print("Composantes du Graphe Réduit :", graphe.graphe_reduit())
        racine = graphe.sommet_racine()
        if racine is not None:
            print(f"Le sommet racine est : {racine + 1}")
            algorithme = input("Choisissez l'algorithme pour le chemin le plus long (bellman-ford/dijkstra) : ").strip()
            print("Distances du chemin le plus long à partir de la racine :", graphe.chemin_le_plus_long(racine, algorithme))
        else:
            print("Aucun sommet racine trouvé.")