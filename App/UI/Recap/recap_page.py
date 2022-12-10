from tkinter import *

import cv2

from App.UI.Common.ListElement import ListElement
from App.UI.Common.ListWidget import ListWidget
from App.UI.Recap.ImageTile.image_tile import ImageTile
from App.UI.page import Page


class RecapPage(Page):
    BACKGROUND_IMG_PATH = "App/UI/Recap/background.png"
    BACK_ARROW_IMG_PATH = "App/UI/Settings/back_arrow.png"
    SAVE_RECAP_IMG_PATH = "App/UI/Settings/save.png"

    def __init__(self, root, cropped_images=None, **kwargs):
        super().__init__(root, **kwargs)
        self.cropped_images = cropped_images

        self.background_img = PhotoImage(file=self.BACKGROUND_IMG_PATH)
        self.back_arrow_img = PhotoImage(file=self.BACK_ARROW_IMG_PATH)
        self.save_recap_img = PhotoImage(file=self.SAVE_RECAP_IMG_PATH)

        self.canvas = Canvas(
            self.root,
            bg="#ffffff",
            height=480,
            width=800,
            bd=0,
            highlightthickness=0,
            relief="ridge")
        self.canvas.place(x=0, y=0)

        self.background = self.canvas.create_image(
            375.0, 231.0,
            image=self.background_img)

        self.back_arrow_btn = Button(
            image=self.back_arrow_img,
            borderwidth=0,
            highlightthickness=0,
            command=lambda: self.to_page(
                page=self.previous_page,
                homepage=self.homepage
            ),
            relief="flat",
            cursor="hand2"
        )

        self.back_arrow_btn.place(
            x=33, y=48,
            width=38,
            height=38
        )

        self.save_recap_btn = Button(
            image=self.save_recap_img,
            borderwidth=0,
            highlightthickness=0,
            command=self.save_cropped_images,
            relief="flat",
            cursor="hand2"
        )

        self.save_recap_btn.place(
            x=286, y=51,
            width=90,
            height=39
        )

        self.images_list_frame = Frame(self.root, bg="white")
        self.images_list_frame.place(
            x=210, y=116.5,
            width=445,
            height=262
        )
        self.images_list = ListWidget(
            parent=self.images_list_frame,
            space_between=1,
            elements=self.get_images()
        )

    def get_images(self):
        images_list = []
        for img_tuple in self.cropped_images:
            images_list.append(
                ListElement(
                    widget=ImageTile,
                    genesis_root=self.root,
                    img_tuple=img_tuple,
                    callback_on_delete=self.delete_shape,
                    height=50,
                )
            )
        return images_list

    def delete_shape(self, shape_to_delete):
        try:
            print(shape_to_delete)
            self.cropped_images.remove(shape_to_delete)
            self.images_list.refresh_list(
                parent_frame=self.images_list_frame,
                elements=self.get_images()
            )
        except ValueError:
            pass

    def save_cropped_images(self):
        for i in range(len(self.cropped_images)):
            cv2.imwrite(f"img{i}.png", self.cropped_images[i][0])
        # save images in a PDF file
