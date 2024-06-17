import numpy as np

def generate_unitary_matrix_with_det(n, target_det):
    if target_det not in [1, -1, 1j, -1j]:
        raise ValueError("Invalid target determinant. Must be 1, -1, i, or -i.")
    
    def random_unitary_matrix(n):
        z = (np.random.randn(n, n) + 1j * np.random.randn(n, n)) / np.sqrt(2.0)
        q, r = np.linalg.qr(z)
        d = np.diagonal(r)
        ph = d / np.abs(d)
        q = np.multiply(q, ph, q)
        return q
    
    unitary_matrix = random_unitary_matrix(n)
    
    det_u = np.linalg.det(unitary_matrix)
    adjustment_factor = np.exp(1j * (np.angle(target_det / det_u) / n))
    adjusted_matrix = unitary_matrix * adjustment_factor
    
    final_det = np.linalg.det(adjusted_matrix)
    assert np.isclose(final_det, target_det), "The determinant of the generated matrix does not match the target determinant."
    
    return adjusted_matrix

target_determinant = 1
unitary_matrix_with_det = generate_unitary_matrix_with_det(4, target_determinant)

unitary_matrix_with_det, np.linalg.det(unitary_matrix_with_det)