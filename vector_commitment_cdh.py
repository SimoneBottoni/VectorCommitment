import math
from typing import List, Tuple, Optional
from charm.toolbox.pairinggroup import PairingGroup, ZR, G1, pair


class VectorCommitmentCDH:
    """Vector Commitment scheme based on CDH.

    Provides key generation, commit, open, and verify operations.
    """

    def __init__(self, group_name: str = 'SS512') -> None:
        self.group = PairingGroup(group_name)
        self.g = self.group.random(G1)

    def key_gen(self, q: int) -> Tuple[List, List, List[List[Optional]]]:
        """Generate keys for a vector of length q.

        Returns:
            z: list of random exponents in ZR (secret exponents)
            h_vec: list where h_vec[i] = g^{z[i]} in G1
            h_mat: q x q matrix where h_mat[i][j] = g^{z[i]*z[j]} for j != i, and None on the diagonal
        """
        z = [self.group.random(ZR) for _ in range(q)]
        h_vec = [self.g ** z_i for z_i in z]

        h_mat: List[List[Optional]] = []
        for i in range(q):
            row: List[Optional] = []
            for j in range(q):
                if i == j:
                    row.append(None)
                else:
                    row.append(self.g ** (z[i] * z[j]))
            h_mat.append(row)

        return z, h_vec, h_mat

    def commit(self, m: List[int], h_vec: List) -> any:
        """Commit to a vector m using public vector h_vec."""
        return math.prod([h_elem ** m_i for h_elem, m_i in zip(h_vec, m)])

    def open(self, i: int, m: List[int], h_mat: List[List[Optional]]) -> any:
        """Open the commitment at position i, producing a proof for m[i]."""
        return math.prod([
            h_ij ** m_j
            for h_ij, m_j in zip(h_mat[i], m)
            if h_ij is not None
        ])

    def verify(self, c, m_i: int, i: int, proof, h_vec: List) -> bool:
        """Verify that proof opens commitment c to value m_i at index i."""
        left = pair(c / (h_vec[i] ** m_i), h_vec[i])
        right = pair(proof, self.g)
        return left == right


# Maintain backward-compatible functional API via a module-level instance.
_vc = VectorCommitmentCDH()


def key_gen(q):
    return _vc.key_gen(q)


def commit(m, h_i):
    return _vc.commit(m, h_i)


def open(i, m, h_i_j):
    return _vc.open(i, m, h_i_j)


def verify(c, m_i, i, l_i, h_i):
    return _vc.verify(c, m_i, i, l_i, h_i)


if __name__ == "__main__":
    # Example usage
    m = [1, 2, 3]
    z, h_vec, h_mat = key_gen(len(m))

    c = commit(m, h_vec)
    l_0 = open(0, m, h_mat)

    check = verify(c, m[0], 0, l_0, h_vec)
    print("Check:", check)
