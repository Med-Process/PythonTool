class FocalLoss(nn.Module):
    def __init__(self, alpha=1, gamma=2, logits=False, reduce=True):
        super(FocalLoss, self).__init__()
        self.alpha = alpha
        self.gamma = gamma
        self.logits = logits
        self.reduce = reduce

    def forward(self, inputs, targets):
        if self.logits:
            BCE_loss = F.binary_cross_entropy_with_logits(inputs, targets, reduce=False)
        else:
            BCE_loss = F.binary_cross_entropy(inputs, targets, reduce=False)
        pt = torch.exp(-BCE_loss)
        F_loss = self.alpha * (1-pt)**self.gamma * BCE_loss


        # inputs_pred = F.sigmoid(inputs)
        # # p = 1-inputs_pred[:,0]
        # p = inputs_pred
        # t = targets

        # pt2 = p*(t==1.).float() + (1-p)*(t==0.).float()
        # loss = -self.alpha*(torch.pow((1-pt2), self.gamma))*torch.log(pt2+1e-12)

        # loss1 = torch.mean(F_loss)
        # loss2 = loss.mean()  # 两种方法求解结果一致

        if self.reduce:
            return torch.mean(F_loss)
        else:
            return F_loss
