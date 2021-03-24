import matplotlib.pyplot as plt

TITLE = "Airway Segmentation"
X_Label = "BCE Weight of Forground"
Y_Label = "Dice of Airway"

save_name = "result.png"

plt.plot([0.5, 0.7, 0.90, 0.99], [0.9070, 0.9066, 0.8989, 0.88], 'ro')

#axis接收的list参数表示：[xmin, xmax, ymin, ymax] 
#设置x、y轴的长度，x轴为[0,6],y轴为[0,20]
# plt.axis([0, 6, 0, 20])
plt.axis([0, 1, 0, 1])


# plt.plot(np.arange(0, N), H.history["loss"], label="loss")

plt.title(TITLE)
plt.xlabel(X_Label)
plt.ylabel(Y_Label)

plt.legend(loc="center right")
plt.savefig(save_name)

print("*************  end  ***********")
