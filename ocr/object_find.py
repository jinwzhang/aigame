import cv2
import numpy as np
from matplotlib import pyplot as plt



def get_rectangle(max_loc, w, h):
    # if method in [cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]:
    #     top_left = min_loc
    # else:
    #     top_left = max_loc
    top_left = max_loc
    bottom_right = (top_left[0] + w, top_left[1] + h)
    return top_left, bottom_right


def get_single_taget_pos(img_arr, template_path, point_or_box=True, threshold=0.7, plot=False):
    # 找与目标图最接近的目标坐标
    template = cv2.imread(template_path)
    b, g, r = cv2.split(template)
    template = cv2.merge([r, g, b])
    template1 = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template1.shape[::-1]
    # 所有的匹配方法
    # methods1 = ['cv2.TM_CCOEFF', 'cv2.TM_CCOEFF_NORMED', 'cv2.TM_CCORR','cv2.TM_CCORR_NORMED', 'cv2.TM_SQDIFF', 'cv2.TM_SQDIFF_NORMED']
    method = 'cv2.TM_CCOEFF_NORMED'
    img = img_arr.copy()
    method = eval(method)  # 去掉字符串的引号
    # 匹配
    res = cv2.matchTemplate(img, template, method)
    # res = np.where(res >= threshold)
    min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(res)
    # print(min_val, max_val, min_loc, max_loc)
    # 使用不同的比较方法，对结果的解释不同
    # 如果方法是 TM_SQDIFF or TM_SQDIFF_NORMED, 取最小值
    top_left, bottom_right = get_rectangle(max_loc, w, h)
    cv2.rectangle(img, top_left, bottom_right, 255, 2)
    if plot:
        plt.subplot(121), plt.imshow(res, cmap='gray'),
        plt.title('Matching Result'), plt.axis('off')
        plt.subplot(122), plt.imshow(img, cmap='gray'),
        plt.title('Detected Point'), plt.axis('off')
        plt.suptitle(method)
        plt.show()
    if max_val >= threshold:
        if point_or_box:
            return (top_left[0] + bottom_right[0])/2, (top_left[1] + bottom_right[1])/2
        else:
            return top_left, bottom_right
    else:
        return None, None


def get_multi_taget_pos(img_arr, template_path, threshold=0.8):
    img_gray = cv2.cvtColor(img_arr, cv2.COLOR_BGR2GRAY)
    img = img_arr.copy()
    template = cv2.imread(template_path)
    b, g, r = cv2.split(template)
    template = cv2.merge([r, g, b])
    template1 = cv2.cvtColor(template, cv2.COLOR_BGR2GRAY)
    w, h = template1.shape[::-1]

    res = cv2.matchTemplate(img, template, cv2.TM_CCOEFF_NORMED)

    loc = np.where(res >= threshold)
    result = []
    for pt in zip(*loc[::-1]):
        result.append([pt, get_rectangle(pt, w, h)])
        cv2.rectangle(img_gray, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
    # plt.subplot(131), plt.imshow(cv2.cvtColor(img_gray, cv2.COLOR_BGR2RGB)),
    # plt.title('Marked'), plt.axis('off')
    # plt.subplot(132), plt.imshow(template, cmap='gray'),
    # plt.title('Template'), plt.axis('off')
    # plt.show()
    return result


if __name__ == '__main__':
    img_arr1 = cv2.imread(r'C:\Users\admin\Desktop\pyProjects\aigame\ocr\Object_tar\full_pic\cur3.PNG')
    b, g, r = cv2.split(img_arr1)
    img_arr1 = cv2.merge([r, g, b])
    get_single_taget_pos(img_arr1, r'C:\Users\admin\Desktop\pyProjects\aigame\ocr\Object_tar\reset0.PNG')
    #  get_multi_taget_pos(img_arr1, r'C:\Users\admin\Desktop\pyProjects\aigame\ocr\Object_tar\mouse2.PNG')
