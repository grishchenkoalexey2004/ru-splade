import torch

# средняя сумма модулей значений вектора (такой же смысл как и в линейной алгебре)
class L1:

    def __call__(self, batch_rep):
        return torch.sum(torch.abs(batch_rep), dim=-1).mean()

# дефолтный регуляризатор (сред количество ненулевых элементов в векторе)
class L0:
    """non-differentiable
    """

    def __call__(self, batch_rep):
        return torch.count_nonzero(batch_rep, dim=-1).float().mean()

# flops - регуляризатор (грубо говря среднее количество операций при подсчёте скалярного произведения векторов q и d)
class FLOPS:
    """constraint from Minimizing FLOPs to Learn Efficient Sparse Representations
    https://arxiv.org/abs/2004.05665
    """

    def __call__(self, batch_rep):
        return torch.sum(torch.mean(torch.abs(batch_rep), dim=0) ** 2)

# планировщик для регуляризатора
class RegWeightScheduler:
    """same scheduling as in: Minimizing FLOPs to Learn Efficient Sparse Representations
    https://arxiv.org/abs/2004.05665
    """

    def __init__(self, lambda_, T):
        self.lambda_ = lambda_
        self.T = T
        self.t = 0
        self.lambda_t = 0

    # ограничивает влияние регуляризации на первых стадиях обучения!
    def step(self):
        """quadratic increase until time T
        """
        if self.t >= self.T:
            pass
        else:
            self.t += 1
            self.lambda_t = self.lambda_ * (self.t / self.T) ** 2
        return self.lambda_t

    def get_lambda(self):
        return self.lambda_t


class SparsityRatio:
    """non-differentiable
    """

    def __init__(self, output_dim):
        self.output_dim = output_dim

    def __call__(self, batch_rep):
        return 1 - torch.sum(batch_rep != 0, dim=-1).float().mean() / self.output_dim

# загрузка регуляризатора
def init_regularizer(reg, **kwargs):
    if reg == "L0":
        return L0()
    elif reg == "sparsity_ratio":
        return SparsityRatio(output_dim=kwargs["output_dim"])
    elif reg == "L1":
        return L1()
    elif reg == "FLOPS":
        return FLOPS()
    else:
        raise NotImplementedError("provide valid regularizer")
