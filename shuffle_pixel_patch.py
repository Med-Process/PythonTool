import numpy as np

# input x: [N, C, H, W]


# Shuffle pixel, 所有patch，相同的shuffle操作
patch_size = 16
data = rearrange(x, 'N C (H P) (W Q) -> N C H W P Q',P=patch_size, Q=patch_size)
data = data.contiguous().view(N, C, H//patch_size, W//patch_size, -1)
indexes = torch.randperm(data.shape[4])
data = data[:,:, :, :, indexes]
data = data.contiguous().view(N, C, H//patch_size, W//patch_size, patch_size, patch_size)
data = rearrange(data, 'N C H W P Q -> N C (H P) (W Q)',P=patch_size, Q=patch_size)


# 所有patch,独立shuffle操作
patch_size = 16
data = rearrange(x, 'N C (H P) (W Q) -> N C H W P Q',P=patch_size, Q=patch_size)
data = data.contiguous().view(N, C, H//patch_size, W//patch_size, -1)
indexes = torch.randperm(data.shape[4] * H//patch_size * W//patch_size)
indexes = indexes.view(H//patch_size, W//patch_size, -1)    # [56, 56, 16]
indexes = torch.argsort(indexes, dim=-1)

id = torch.arange(H*W)
id = id.view(H//patch_size, W//patch_size, -1)
global_index = torch.gather(id, dim=2, index=indexes)
global_index = global_index.view(-1)       # 全局索引，局部排序

data = data.view(N, C, -1)
data = data[:,:, global_index]
data = data.contiguous().view(N, C, H//patch_size, W//patch_size, patch_size, patch_size)
data = rearrange(data, 'N C H W P Q -> N C (H P) (W Q)',P=patch_size, Q=patch_size)


# patch shuffle
data = rearrange(data, 'N C (H P) (W Q) -> N C P Q H W',P=patch_size, Q=patch_size)
data = data.contiguous().view(N, C, patch_size, patch_size, -1)
indexes_patch = torch.randperm(data.shape[4])
indexes_patch = torch.argsort(indexes_patch, dim=-1)
data = data[:, :, :, :, indexes_patch]
data = rearrange(data, 'N C P Q (H W) -> N C (H P) (W Q)', H=H//patch_size, W=W//patch_size)

