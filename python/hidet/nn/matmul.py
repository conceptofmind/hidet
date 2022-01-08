from hidet.ir.type import tensor_type
from hidet.ir.expr import Axis, scalar_var
from hidet.ir.dialects.compute import tensor_input, compute, reduce_sum
from hidet.ir.task import Task, Grid


def matmul(N: int, M: int, K: int) -> Task:
    A = tensor_input('A', 'float32', [N, K])
    B = tensor_input('B', 'float32', [K, M])
    k = Axis(K)
    C = compute('C', [N, M], lambda i, j: reduce_sum(A[i, k] * B[k, j], axis=k))
    return Task(
        name='matmul.grid',
        computation=C,
        params=[A, B, C],
        params_type=[tensor_type('global', 'float32', [N, K], strides=[K, 1]),
                     tensor_type('global', 'float32', [K, M], strides=[M, 1]),
                     tensor_type('global', 'float32', [N, M], strides=[M, 1])],
        worker=Grid()
    )


def generic_matmul() -> Task:
    N = scalar_var('N', 'int32')
    M = scalar_var('M', 'int32')
    K = scalar_var('K', 'int32')
    A = tensor_input('A', 'float32', [N, K])
    B = tensor_input('B', 'float32', [K, M])
    k = Axis(K)
    C = compute('C', [N, M], lambda i, j: reduce_sum(A[i, k] * B[k, j], axis=k))
    return Task(
        name='matmul.grid',
        computation=C,
        params=[A, B, C],
        params_type=[tensor_type('global', 'float32', [N, K], strides=[K, 1]),
                     tensor_type('global', 'float32', [K, M], strides=[M, 1]),
                     tensor_type('global', 'float32', [N, M], strides=[M, 1])],
        worker=Grid()
    )

