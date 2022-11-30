from tkinter import *
import cv2


class ImageTile(Frame):
    BACKGROUND_IMG_PATH = "App/UI/Recap/ImageTile/background.png"
    DELETE_BTN_IMG_PATH = "App/UI/Recap/ImageTile/delete_btn.png"
    IMAGE_ICON_IMG_PATH = "App/UI/Recap/ImageTile/image_icon.png"

    def __init__(self, genesis_root=None, img_tuple=None, callback_on_delete=None, **kwargs):
        super().__init__(**kwargs)
        self.genesis_root = genesis_root
        self.img = img_tuple[0]
        self.img_name = img_tuple[1]
        self.callback_on_delete = callback_on_delete  # call it when delete btn is pressed, it deletes the shape from array in RecapPage

        self.background_img = PhotoImage(file=self.BACKGROUND_IMG_PATH)
        self.delete_btn_img = PhotoImage(file=self.DELETE_BTN_IMG_PATH)
        self.image_icon_img = PhotoImage(file=self.IMAGE_ICON_IMG_PATH)

        self.background = Label(
            self,
            image=self.background_img,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            cursor="hand2"
        )
        self.background.pack()

        self.icon_label = Label(
            self,
            image=self.image_icon_img,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            cursor="hand2"
        )
        self.icon_label.place(
            x=23, y=12
        )

        self.shape_label = Label(
            self,
            text=f"{self.img_name}",
            font=("Lucida Console", 9),
            bg="white",
            cursor="hand2"
        )
        self.shape_label.place(
            x=66, y=17
        )

        self.delete_btn = Button(
            self,
            image=self.delete_btn_img,
            bd=0,
            highlightthickness=0,
            relief="ridge",
            command=lambda: self.callback_on_delete(img_tuple),
            cursor="hand2"
        )
        self.delete_btn.place(
            x=330, y=12
        )

        self.background.bind("<Button-1>", self.click)
        self.icon_label.bind("<Button-1>", self.click)
        self.shape_label.bind("<Button-1>", self.click)

    def click(self, event):
        cv2.imshow(f"{self.img_name}", self.img)
