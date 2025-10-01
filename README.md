# VectorCommitment

Implementation of Vector Commitment based on CDH<sup>1</sup>.

A vector commitment lets you commit once to an entire vector m and later open just one position i with a short proof that verifies against the original commitment.

<sup>1</sup>Catalano, D., Fiore, D. (2013). Vector Commitments and Their Applications. In: Kurosawa, K., Hanaoka, G. (eds) Public-Key Cryptography – PKC 2013. PKC 2013. Lecture Notes in Computer Science, vol 7778. Springer, Berlin, Heidelberg. https://doi.org/10.1007/978-3-642-36362-7_5

### Requirements
Charm-Crypto v.0.50 (https://github.com/JHUISI/charm)

## Usage
A simple class-based API is provided in `vector_commitment_cdh.py`:

```python
from vector_commitment_cdh import VectorCommitmentCDH

vc = VectorCommitmentCDH('SS512')

m = [1, 2, 3]
_, h_vec, h_mat = vc.key_gen(len(m))

c = vc.commit(m, h_vec)
proof_i = vc.open(0, m, h_mat)
assert vc.verify(c, m[0], 0, proof_i, h_vec)
```

For backward compatibility, the legacy functions `key_gen`, `commit`, `open`, and `verify` remain available at module level and delegate to the class implementation.

## API
- VectorCommitmentCDH.key_gen(q) -> (z, h_vec, h_mat)
- VectorCommitmentCDH.commit(m, h_vec) -> commitment
- VectorCommitmentCDH.open(i, m, h_mat) -> proof for index i
- VectorCommitmentCDH.verify(c, m_i, i, proof, h_vec) -> bool

## Disclaimer
This is a research-grade implementation, meant for experimentation and educational use.
Not suitable for production deployment.

---

## Acknowledgements

This work was supported in part by project SERICS (PE00000014) under the NRRP MUR program funded by the EU - NGEU. Views and opinions expressed are however those of the authors only and do not necessarily reflect those of the European Union or the Italian MUR. Neither the European Union nor the Italian MUR can be held responsible for them.
