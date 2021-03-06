# -*- coding: utf-8 -*-
from PIL import Image, ImageFile
import os
import torch
from datasets.cityscapes_Dataset import City_Dataset, to_tuple

ImageFile.LOAD_TRUNCATED_IMAGES = True

crosscity_set_13 = [0, 1, 2, 6, 7, 8, 10, 11, 12, 13, 15, 17, 18]
synthia_set_13 = [0, 1, 2, 6, 7, 8, 10, 11, 12, 13, 15, 17, 18]
class GTA5_Dataset(City_Dataset):
    def __init__(
        self,
        root='/local_datasets/GTA5',
        list_path='./datasets/GTA5/list',
        split='train',
        base_size=769,
        crop_size=769,
        training=True,
        random_mirror=False,
        random_crop=False,
        resize=False,
        gaussian_blur=False,
        class_16=False,
        class_13=False
    ):

        # Args
        self.data_path = root
        self.list_path = list_path
        self.split = split
        self.base_size = to_tuple(base_size)
        self.crop_size = to_tuple(crop_size)
        self.training = training
        self.class_16 = False
        self.class_13 = class_13
        assert class_16 == False

        # Augmentation
        self.random_mirror = random_mirror
        self.random_crop = random_crop
        self.resize = resize
        self.gaussian_blur = gaussian_blur

        # Files
        item_list_filepath = os.path.join(self.list_path, self.split + ".txt")
        if not os.path.exists(item_list_filepath):
            raise Warning("split must be train/val/trainval/test/all")
        self.image_filepath = os.path.join(self.data_path, "images")
        self.gt_filepath = os.path.join(self.data_path, "labels")
        self.items = [id.strip() for id in open(item_list_filepath)]

        # Label map
        """
        if self.class_13:
           
            self.id_to_trainid = {7: 0, 8: 1, 11: 2, 19: 3, 20: 4, 21: 5, 23: 6,
                              24: 7, 25: 8, 26: 9, 28: 10, 32: 11, 33: 12}
        else:
        """
        self.id_to_trainid = {
            7: 0, 8: 1, 11: 2, 12: 3, 13: 4, 17: 5, 19: 6, 20: 7, 21: 8,
            22: 9, 23: 10, 24: 11, 25: 12, 26: 13, 27: 14, 28: 15, 31: 16, 32: 17, 33: 18
        }
        self.class_13 = class_13
        self.trainid_to_13id = {id: i for i, id in enumerate(crosscity_set_13)}
        # Print
        print("{} num images in GTA5 {} set have been loaded.".format(
            len(self.items), self.split))

    def __getitem__(self, item):
        id = int(self.items[item])
        name = f"{id:0>5d}.png"

        # Open image and label
        image_path = os.path.join(self.image_filepath, name)
        gt_image_path = os.path.join(self.gt_filepath, name)
        image = Image.open(image_path).convert("RGB")
        gt_image = Image.open(gt_image_path)

        # Augmentation
        if (self.split == "train" or self.split == "trainval" or self.split == "all") and self.training:
            image, gt_image = self._train_sync_transform(image, gt_image)
        else:
            image, gt_image = self._val_sync_transform(image, gt_image)
        return image, gt_image, item
