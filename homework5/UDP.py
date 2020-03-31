import matplotlib.pyplot as plot
import random

num1 = 0B0110011001100000
num2 = 0B0101010101010101
num3 = 0B1000111100001100
udpSeg = [num1, num2, num3]


def check_udp_sender(segment_list):
    udp_check = complement(check_udp(segment_list[0], segment_list[1], segment_list[2]))
    udpSeg.append(udp_check)
    return


def complement(num):
    return 0xffff - num & 0xffffffff


def check_udp(num01, num02, num03):
    num04 = num01 + num02
    num04 = num04 % (2**16) + (num04 >> 16)
    num04 = num03 + num04
    num04 = num04 % (2**16) + (num04 >> 16)
    bin(num04)
    return num04


def distinguish(segment_list, add_in_mistake):
    num_result = 0
    for num in segment_list:
        # 以一个极低的概率使得接收到的数据发生变异！
        if add_in_mistake:
            if random.random() < 0.1:
                num += 1
        num_result += num
        num_result = num_result % (2 ** 16) + (num_result >> 16)
    udpSeg.append(num_result)
    return num_result == 2 ** 16 - 1, num_result


def draw_use_matplot(segment_list):
    draw_data_list = list()
    for seg in segment_list:
        temp_str = str(bin(seg))
        print(temp_str)
        list_str = list(temp_str)
        while len(list_str) < 18:
            list_str.insert(2, "0")
        index = 0
        bit_list = list()
        for char in list_str:
            if index <= 1:
                index += 1
                continue
            bit_list.append(int(char))
        print(bit_list)
        draw_data_list.append(bit_list)
    subplot_index = 1
    x_list = list(range(1, 17))
    fig = plot.figure()
    plot.legend("UDP data segments and verification")
    for data_list in draw_data_list:
        plot.subplot(5, 1, subplot_index)
        plot.bar(x_list, data_list)
        plot.xticks(x_list)
        if subplot_index <= 3:
            plot.ylabel('seg' + str(subplot_index))
        elif subplot_index == 4:
            plot.ylabel('checksum')
        elif subplot_index == 5:
            plot.ylabel('check result')
            plot.xlabel("if check result is all full, then the check should pass! OTHERWISE, it should not!!")
        subplot_index += 1
    plot.show()


if __name__ == "__main__":
    for seg in udpSeg:
        print(bin(seg))
    check_udp_sender(udpSeg)
    distinguish_result = distinguish(udpSeg, True)
    if distinguish_result[0]:
        print("nothing wrong")
    else:
        print("mistake occurs")
    draw_use_matplot(udpSeg)
