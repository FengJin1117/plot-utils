import numpy as np

# 最大色差重排
def interleave_order(n, mode="high_low"):
    """
    Generate an order that maximizes adjacent distance.
    
    n: number of colors
    mode:
        - "high_low": 深浅交错（推荐，论文稳）
        - "center_out": 从中间向两侧扩散
    """
    idx = np.arange(n)

    if mode == "high_low":
        # [0,1,2,3,4,5,6,7,8,9]
        mid = (n - 1) // 2
        left = idx[:mid + 1][::-1]   # 深色
        right = idx[mid + 1:]        # 浅色

        order = []
        for l, r in zip(left, right):
            order.extend([l, r])
        if len(left) > len(right):
            order.append(left[-1])

    elif mode == "center_out":
        center = n // 2
        order = [center]
        for i in range(1, n):
            j = center + (-1)**i * i
            if 0 <= j < n:
                order.append(j)

    else:
        raise ValueError(f"Unknown mode: {mode}")

    return np.array(order)
