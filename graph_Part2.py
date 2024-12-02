import itertools

class Graphe:
    def __init__(self):
        # Initialize graph attributes
        self.type_graphe = None  # 'orienté' or 'non orienté'
        self.representation_graphe = None  # 'adjacence', 'incidence', or 'dictionnaire'
        self.matrice_adjacence = []
        self.n = 0  # Number of vertices

    def acquérir_graphe(self):
        """
        Collect graph information from user input
        Supports different input methods for graph representation
        """
        try:
            # Get graph type
            while True:
                self.type_graphe = input("Entrez le type de graphe (orienté/non orienté) : ").strip().lower()
                if self.type_graphe in ['orienté', 'non orienté']:
                    break
                print("Type de graphe invalide. Réessayez.")

            # Get input method
            while True:
                self.representation_graphe = input("Entrez la méthode d'entrée (adjacence/incidence/dictionnaire) : ").strip().lower()
                if self.representation_graphe in ['adjacence', 'incidence', 'dictionnaire']:
                    break
                print("Méthode d'entrée invalide. Réessayez.")

            # Call appropriate input method based on user choice
            input_methods = {
                'adjacence': self._entrer_matrice_adjacence,
                'incidence': self._entrer_matrice_incidence,
                'dictionnaire': self._entrer_dictionnaire
            }
            input_methods[self.representation_graphe]()

        except Exception as e:
            print(f"Erreur lors de l'acquisition du graphe : {e}")

    def _entrer_matrice_adjacence(self):
        """Input graph using adjacency matrix"""
        self.n = int(input("Entrez le nombre de sommets : "))
        print("Entrez la matrice d'adjacence ligne par ligne (séparée par des espaces) :")
        self.matrice_adjacence = [
            list(map(int, input(f"Ligne {i+1} : ").split())) 
            for i in range(self.n)
        ]

    def verifier_isomorphisme(self, autre_graphe):
        """
        Check if two graphs are isomorphic
        Returns:
        - Boolean indicating isomorphism
        - Vertex mapping (BX)
        - Edge mapping (BE)
        """
        # Quick checks before detailed verification
        if self.n != autre_graphe.n:
            return False, None, None

        # Try all possible vertex permutations
        for permutation in itertools.permutations(range(autre_graphe.n)):
            # Create vertex mapping
            bx = {i: permutation[i] for i in range(self.n)}
            
            # Check if this permutation preserves graph structure
            if self._verifier_structure_isomorphisme(autre_graphe, permutation):
                # Create edge mapping
                be = self._trouver_bijection_aretes(autre_graphe, permutation)
                return True, bx, be

        return False, None, None

    def _verifier_structure_isomorphisme(self, autre_graphe, permutation):
        """Verify if graph structure is preserved under a specific permutation"""
        for u in range(self.n):
            for v in range(self.n):
                # Compare edge weights after permutation
                if self.matrice_adjacence[u][v] != autre_graphe.matrice_adjacence[permutation[u]][permutation[v]]:
                    return False
        return True

    def verifier_graphe_eulerien(self):
        """
        Check if graph is Eulerian based on graph type
        Returns boolean indicating Eulerian property
        """
        # Calculate vertex degrees
        degres = [sum(ligne) for ligne in self.matrice_adjacence]

        if self.type_graphe == "non orienté":
            # Non-oriented graph: all vertices must have even degree
            sommets_impairs = sum(1 for degre in degres if degre % 2 != 0)
            return sommets_impairs == 0

        elif self.type_graphe == "orienté":
            # Oriented graph: in-degree and out-degree must match
            in_degres = [sum(self.matrice_adjacence[j][i] for j in range(self.n)) for i in range(self.n)]
            return all(in_degres[i] == degres[i] for i in range(self.n))

def main():
    """Main function to demonstrate graph operations"""
    try:
        # Acquire first graph
        print("--- Acquisition du premier graphe ---")
        graphe1 = Graphe()
        graphe1.acquérir_graphe()

        # Acquire second graph
        print("\n--- Acquisition du deuxième graphe ---")
        graphe2 = Graphe()
        graphe2.acquérir_graphe()

        # Isomorphism test
        print("\n--- Test d'Isomorphisme ---")
        est_iso, bx, be = graphe1.verifier_isomorphisme(graphe2)
        
        if est_iso:
            print("Les graphes sont ISOMORPHES !")
            print("Bijection des sommets (BX):", bx)
            print("Bijection des arêtes (BE):", be)
        else:
            print("Les graphes ne sont PAS isomorphes.")

        # Eulerian graph test
        print("\n--- Test de Graphe Eulerien ---")
        print(f"Graphe 1 - Est Eulerien : {graphe1.verifier_graphe_eulerien()}")
        print(f"Graphe 2 - Est Eulerien : {graphe2.verifier_graphe_eulerien()}")

    except Exception as e:
        print(f"Une erreur s'est produite : {e}")

if __name__ == "__main__":
    main()