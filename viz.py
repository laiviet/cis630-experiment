import matplotlib.pyplot as plt

data = [2043,
        1957,
        1990,
        1983,
        1999,
        1657,
        1655,
        1677,
        1657,
        1655,
        3666,
        3672,
        3682,
        3666,
        3978,
        2995,
        2951,
        2963,
        3033,
        3012,
        2108,
        2148,
        2143,
        2148,
        2160,
        1744,
        1768,
        1768,
        1748,
        1749,
        4399,
        4310,
        4142,
        3960,
        4008,
        3053,
        3100,
        3159,
        3098,
        3158,
        ]

data_acc = [
    0.5188106894493103,
    0.5170115232467651,
    0.513677179813385,
    0.5186681151390076,
    0.5225697755813599,
    0.505778431892395,
    0.501617968082428,
    0.4894600510597229,
    0.48488348722457886,
    0.49126294255256653,
    0.5146055817604065,
    0.5201456546783447,
    0.5208556056022644,
    0.508043110370636,
    0.5134223103523254,
    0.5049926042556763,
    0.48284947872161865,
    0.48391273617744446,
    0.49782732129096985,
    0.4816475510597229

]

import numpy as np

if __name__ == '__main__':
    # data = np.array(data).reshape(8, 5)
    # avg = data.mean(axis=1)
    # std = data.std(axis=1)
    #
    # labels = ['b-1-2', 'b-1-4', 'b-2-1', 'b-2-2', 'd-1-2', 'd-1-4', 'd-2-1', 'd-2-2']
    # print(avg)
    # print(std)
    #
    # plt.errorbar(labels[:4], avg[:4] - avg[:4], std[:4], linestyle='None', marker='^')
    # plt.errorbar(labels[4:], avg[4:] - avg[:4], std[4:], linestyle='None', marker='^')
    # plt.legend(['bare-metal', 'docker container'], loc='upper left')
    # plt.title('Duration difference between bare-metal and container')
    # plt.xlabel('Setting')
    # plt.ylabel('Duration difference (sec)')
    # plt.show()

    data = np.array(data_acc).reshape(4, 5)
    avg = data.mean(axis=1)
    std = data.std(axis=1)

    labels = ['1-2', '1-4', '2-1', '2-2']
    print(avg)
    print(std)

    import matplotlib.patches as mpatches

    red_patch = mpatches.Patch(color='green', label='2 GPUs')
    blue_patch = mpatches.Patch(color='blue', label='4 GPUs')

    plt.legend(handles=[red_patch, blue_patch])
    plt.bar(labels, avg, color=['green', 'blue', 'green', 'blue'])
    plt.errorbar(labels, avg, std, linestyle='None', ecolor='black')
    plt.title('Accuracy vs configuration')
    plt.xlabel('Hardware configuration')
    plt.ylabel('Accuracy')
    plt.ylim((0.4,0.55))
    plt.show()
