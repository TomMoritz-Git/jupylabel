import pandas as pd
import numpy as np
import ipywidgets as widgets
import os
from IPython.display import Image
from ipywidgets import interact, interact_manual
import glob
from pathlib import Path
import shutil



def run():
    global label_list

    display(widgets.HTML('''<style>
        :root {--jp-widgets-inline-label-width: 100px !important;}
    </style>'''))

    header = widgets.Image(
        value=open("./ressources/header.jpg", "rb").read(),
        width='auto',
        layout={'margin': '0 0 25px 0'}
    )

    data_folder_input = widgets.Text(
        description='Data folder:',
        placeholder='./data',
    )

    dest_dir_input = widgets.Text(
        description='Destination directory:',
        placeholder='./',
        value='./'
    )

    img_path_dd = widgets.Dropdown(
        description='Image path:',
        disabled=True,
    )

    next_img_btn = widgets.Button(
        description='Next image',
        button_style='success',
        disabled=True,
    )

    prev_img_btn = widgets.Button(
        description='Previous image',
        button_style='success',
        disabled=True,
    )

    img_display = widgets.Image(
        value=open("./ressources/404.png", "rb").read(),
        width='80%',
        layout={'margin': '12.5px 0 0 0'}
    )
    vars(img_display)['is_image'] = False

    new_label_input = widgets.Text(
        description='Label name:',
        placeholder='Cats',
    )

    create_label_btn = widgets.Button(
        description='Create label',
        button_style='success',
        disabled=True,
    )

    create_label_btn.layout = widgets.Layout(width='100px')

    label_list = []

    def select_new_img(e, from_label=False):
        src = 'Next image' if from_label else vars(e)['_trait_values']['description']
        curr_idx = img_path_dd.options.index(img_path_dd.value)
        if src == 'Next image':
            new_idx = curr_idx + 1 if (curr_idx + 1) < len(img_path_dd.options) else 0
        else:
            new_idx = curr_idx - 1 if curr_idx > 0 else len(img_path_dd.options) - 1
        img_path_dd.value = img_path_dd.options[new_idx]

    def update_img_path_dd(img_paths):
        img_path_dd.options = img_paths
        if img_paths:
            img_path_dd.disabled = False
            next_img_btn.disabled = False
            prev_img_btn.disabled = False
        else:
            img_path_dd.disabled = True
            next_img_btn.disabled = True
            prev_img_btn.disabled = True

    def load_img(path):
        allowed_ext = ['.jpg', '.png', '.jpeg']
        img_paths = glob.glob(os.path.join(path, '*.*'))
        img_paths = [x for x in img_paths if os.path.splitext(x)[-1] in allowed_ext]
        update_img_path_dd(img_paths)

    def check_data_folder(e):
        try:
            path = e['owner'].value
            if os.path.exists(path):
                load_img(path)
            else:
                update_img_path_dd([])
        except:
            pass

    def update_img_display(e):
        new_img_path = img_path_dd.value if img_path_dd.value else './ressources/404.png'
        new_img = open(new_img_path, "rb").read()
        img_display.value = new_img
        if new_img_path == './ressources/404.png':
            vars(img_display)['is_image'] = False
        else:
            vars(img_display)['is_image'] = True

    def create_label_toggle(e):
        val = new_label_input.value
        if val:
            create_label_btn.disabled = False
        else:
            create_label_btn.disabled = True
            
    def create_label(e):
        global label_list
        new_label = new_label_input.value
        label_list.append(new_label)
        label_box.children = get_label_btns()
        new_label_input.value = ''    
            
    def del_label(e):
        global label_list
        label_to_del = e.tooltip.split('Delete the label ')[-1]
        label_list = [label for label in label_list if label != label_to_del]
        label_box.children = get_label_btns()
            
    def get_label_btns():
        btns = []
        for label in label_list:
            if label:
                btn_left = widgets.Button(
                    description=label,
                    button_style='')
                btn_right = widgets.Button(
                    description='X',
                    button_style='danger',
                    tooltip='Delete the label ' + label,
                    layout={'width': '30px'})
                btn_right.on_click(del_label)
                btn_left.on_click(label_image)
                btns.append(widgets.HBox([btn_left, btn_right]))
        return btns

    def label_image(e):
        label = e.description
        if img_display.is_image and img_path_dd.value:
            dest_dir = dest_dir_input.value
            dest_path = os.path.join(dest_dir, label)
            Path(dest_path).mkdir(parents=True, exist_ok=True)
            shutil.copy(img_path_dd.value, dest_path)
        select_new_img(None, from_label=True)
            
    data_folder_input.observe(check_data_folder)
    img_path_dd.observe(update_img_display)
    new_label_input.observe(create_label_toggle)
    next_img_btn.on_click(select_new_img)
    prev_img_btn.on_click(select_new_img)
    create_label_btn.on_click(create_label)
    new_label_input.on_submit(create_label)


    left_pannel = widgets.VBox([
        data_folder_input,
        dest_dir_input,
        img_path_dd,
        widgets.HBox([prev_img_btn, next_img_btn]),
        img_display
    ])

    label_box = widgets.VBox(get_label_btns())
    label_box.layout = widgets.Layout(margin='20px 0 0 0')

    right_pannel = widgets.VBox([
        widgets.HBox([new_label_input, create_label_btn]),
        label_box
    ])

    left_pannel.layout = widgets.Layout(width='50%')
    right_pannel.layout = widgets.Layout(width='50%')


    return widgets.VBox([header, widgets.HBox([left_pannel, right_pannel])])
