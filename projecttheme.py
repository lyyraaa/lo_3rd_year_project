# Defines some of the attributes and the images to use for UI objects
projecttheme = (
    {"font": "Lucida Grande",
    "font_size": 12,
    "text_color": [255, 255, 255, 255],
    "gui_color": [255, 255, 255, 255],
    "button": {
        "text_color": [0, 0, 0, 255],
        "down": {
            "image": {
                "source": "editorbutton0-down.png",
                "frame": [8, 6, 2, 2],
                "padding": [2, 2, 2, 2]
                },
            },
        "up": {
            "image": {
                "source": "editorbutton0.png",
                "frame": [6, 5, 6, 3],
                "padding": [2, 2, 2, 2]
                }
            }
        },
    "slider": {
        "knob": {
            "image": {
                "source": "editorbutton0-down.png"
            },
            "offset": [-5, -11]
        },
        "padding": [8, 8, 8, 8],
        "step": {
            "image": {
                "source": "slider-knob.png"
            },
            "offset": [-2, -8]
        },
        "bar": {
            "image": {
                "source": "slider-bar.png",
                "frame": [8, 8, 8, 0],
                "padding": [8, 8, 8, 8]
            }
        }
    },
    "vscrollbar": {
        "knob": {
            "image": {
                "source": "vscrollbar.png",
                "region": [0, 16, 16, 16],
                "frame": [0, 6, 16, 4],
                "padding": [0, 0, 0, 0]
            },
            "offset": [0, 0]
        },
        "bar": {
            "image": {
                "source": "vscrollbar.png",
                "region": [0, 64, 16, 16]
            },
            "padding": [0, 0, 0, 0]
        }
    },
    "checkbox": {
        "checked": {
            "image": {
                "source": "checkbox-checked.png"
            }
        },
        "unchecked": {
            "image": {
                "source": "checkbox.png"
            }
        }
    }
    },'theme/')
