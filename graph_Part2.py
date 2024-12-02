from collections import defaultdict, deque
import itertools

class Graphe:
    # ... [previous existing methods remain the same]

    # Method to check graph isomorphism
    def verifier_isomorphisme(self, autre_graphe):
        # If graphs have different number of vertices, they can't be isomorphic
        if self.n != autre_graphe.n:
            return False, None, None

        # Generate all possible vertex mappings
        for permutation in itertools.permutations(range(autre_graphe.n)):
            # Bijection for vertices
            bx = {i: permutation[i] for i in range(self.n)}
            
            # Check if this permutation preserves graph structure
            if self._verifier_structure_isomorphisme(autre_graphe, permutation):
                # Bijection for edges
                be = self._trouver_bijection_aretes(autre_graphe, permutation)
                return True, bx, be

        return False, None, None

    def _verifier_structure_isomorphisme(self, autre_graphe, permutation):
        # Check if graph structure is preserved under this permutation
        for u in range(self.n):
            for v in range(self.n):
                # Map original graph vertices to permuted vertices
                if self.matrice_adjacence[u][v] != autre_graphe.matrice_adjacence[permutation[u]][permutation[v]]:
                    return False
        return True

    def _trouver_bijection_aretes(self, autre_graphe, permutation):
        # Create bijection mapping for edges
        bijection = {}
        for u in range(self.n):
            for v in range(self.n):
                if self.matrice_adjacence[u][v] > 0:
                    # Map original edge to corresponding edge in permuted graph
                    bijection[(u,v)] = (permutation[u], permutation[v])
        return bijection

    # Method to check if graph is Eulerian
    def verifier_graphe_eulerien(self):
        degres = [sum(ligne) for ligne in self.matrice_adjacence]
        
        # Eulerian graph conditions
        if self.type_graphe == "non orienté":
            # Non-oriented graph: all vertices must have even degree
            sommets_impairs = sum(1 for degre in degres if degre % 2 != 0)
            return sommets_impairs == 0

        elif self.type_graphe == "orienté":
            # Oriented graph: in-degree and out-degree must match for each vertex
            in_degres = [sum(self.matrice_adjacence[j][i] for j in range(self.n)) for i in range(self.n)]
            return all(in_degres[i] == degres[i] for i in range(self.n))

# Modify main script to match project requirements
if __name__ == "__main__":
    # Acquisition et test du premier graphe
    print("Acquisition du premier graphe :")
    graphe1 = Graphe()
    graphe1.acquérir_graphe()
    
    # Acquisition et test du deuxième graphe
    print("\nAcquisition du deuxième graphe :")
    graphe2 = Graphe()
    graphe2.acquérir_graphe()
    
    # Test Isomorphisme
    est_iso, bx, be = graphe1.verifier_isomorphisme(graphe2)
    print("\nRésultats Isomorphisme :")
    if est_iso:
        print("Les graphes sont isomorphes.")
        print("Bijection des sommets (BX):", bx)
        print("Bijection des arêtes (BE):", be)
    else:
        print("Les graphes ne sont pas isomorphes.")
    
    # Test Graphe Eulerien
    print("\nTest Graphe Eulerien :")
    print(f"Graphe 1 - Est Eulerien : {graphe1.verifier_graphe_eulerien()}")
    print(f"Graphe 2 - Est Eulerien : {graphe2.verifier_graphe_eulerien()}")