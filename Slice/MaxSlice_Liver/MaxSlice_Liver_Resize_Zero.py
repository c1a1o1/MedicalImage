# -*- coding: utf-8 -*-
from Slice.MaxSlice_Liver.MaxSlice_Liver_Base import MaxSlice_Liver_Base
import numpy as np
from PIL import Image
from Config import Config
from Tools import save_image, get_distribution_label, mark_outer_zero, show_image
import os


class MaxSlice_Liver_Resize_Zero(MaxSlice_Liver_Base):
    def __init__(self, config):
        self.config = config

        MaxSlice_Liver_Base.__init__(self, config)
        self.images, self.masks, self.labels = MaxSlice_Liver_Base.load_image_mask_label(config)
        print 'load images shape is ', np.shape(self.images)
        if not self.load_npy_file():
            self.roi_images = MaxSlice_Liver_Resize_Zero.resize_images(self.images, self.masks, config.MaxSlice_Resize_Zero['RESIZE'], self.config)
        print np.shape(self.roi_images)
        # self.save_ROI_image(self.config.MaxSlice_Resize_Zero['IMAGE_SAVE_PATH'])
        self.start_index = 0
        self.save_npy_file()
        self.epoch_num = 0
        self.roi_images = np.array(self.roi_images)
        self.labels = np.array(self.labels)
        self.shuffle_ROI()
        self.split_train_and_validation()

    # 加载ｎｕｍｐｙ文件，若是不存在，则返回ｆａｌｓｅ
    def load_npy_file(self):
        if not os.path.exists(self.config.MaxSlice_Liver_Resize_Zero['SAVE_NPY_PATH'][2]):
            return False
        if not os.path.exists(self.config.MaxSlice_Liver_Resize_Zero['SAVE_NPY_PATH'][1]):
            return False
        self.roi_images = np.load(
            self.config.MaxSlice_Liver_Resize_Zero['SAVE_NPY_PATH'][0]
        )
        self.labels = np.load(
            self.config.MaxSlice_Liver_Resize_Zero['SAVE_NPY_PATH'][1]
        )
        return True
    # 保存为ｎｕｍｐｙ文件
    def save_npy_file(self):
        np.save(
            self.config.MaxSlice_Liver_Resize_Zero['SAVE_NPY_PATH'][0],
            self.roi_images
        )
        np.save(
            self.config.MaxSlice_Liver_Resize_Zero['SAVE_NPY_PATH'][1],
            self.labels
        )
    @staticmethod
    def resize_images(images, masks, new_size, config):
        roi_images = []
        print np.shape(images)
        print np.shape(masks)
        for index, phase_images in enumerate(images):
            print index
            cur_roi_images = []
            for phase_index, image in enumerate(phase_images):
                mask_image = masks[index][phase_index]
                image = np.array(image)
                [ys, xs] = np.where(mask_image != 0)
                miny = np.min(ys)
                maxy = np.max(ys)
                minx = np.min(xs)
                maxx = np.max(xs)
                if index != 145:
                    image, _ = mark_outer_zero(image, mask_image)
                else:
                    image[np.where(mask_image == 0)] = 0
                # show_image(image * 120)
                # show_image(mask_image * 255)
                ROI = image[miny - 2:maxy + 2, minx - 2:maxx + 2]
                ROI_Image = Image.fromarray(np.asarray(ROI, np.float32))
                ROI_Image = ROI_Image.resize(new_size)
                # show_image(np.array(ROI_Image) * 120)
                cur_roi_images.append(np.array(ROI_Image))
                save_image(
                    np.array(ROI_Image)*120,
                    os.path.join(config.MaxSlice_Liver_Resize_Zero['IMAGE_SAVE_PATH'], str(index) + '_' + str(phase_index) + '.jpg')
                )
            roi_images.append(cur_roi_images)
        return roi_images

    @staticmethod
    def test_unit():
        # MaxSlice_Resize(Config)
        dataset = MaxSlice_Liver_Resize_Zero(Config)
        batch_size = 20
        for i in range(100):
            images, labels = dataset.get_next_batch(batch_size)
            print np.shape(images), np.shape(labels)
            print get_distribution_label(labels)

if __name__ == '__main__':
    MaxSlice_Liver_Resize_Zero.test_unit()
