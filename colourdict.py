################################################################################
### Color dictionary file, to edit colors independently and keep consistency ###
################################################################################

# Takes aliases as a keyword argument,
# a dictionary of state numbers and the colour they should appear as
# so as to overwrite default colours

class colourdict:

    def __init__(self,aliases=None):

        self.colours = {
            "-1":(0,0,0,255),
            #"0":(220,220,220,0),
            "1":(255,160,180,0),
            "2":(160,255,160,0),
            "3":(160,160,255,0),
            "4":(160,255,255,0),
            "5":(255,160,255,0),
            "6":(255,255,160,0),
            "7":(105,105,105,0),
            "8":(255,255,255,0),
            "9":(60,200,200,0),
            "10":(45,150,150,0),
            "11":(254,216,176,0),
            "12":(248,213,104,0),
            "13":(255,174,66,0),
            "14":(255,159,0,0),
            "15":(255,103,0,0),
            "16":(190, 48, 255,0),
            "17":(154, 39, 207,0),
            "18":(108, 28, 145,0),
            "19":(50, 200, 50,0),
            "20": (123, 104, 238, 0),
            "21": (245, 222, 179, 0),
            "22": (255, 140, 0, 0),
            "23": (50, 205, 50, 0),
            "24": (105, 105, 105, 0),
            "25": (0, 0, 255, 0),
            "26": (173, 216, 230, 0),
            "27": (154, 205, 50, 0),
            "28": (248, 248, 255, 0),
            "29": (0, 0, 205, 0),
            "30": (250, 250, 210, 0),
            "31": (240, 248, 255, 0),
            "32": (205, 92, 92, 0),
            "33": (95, 158, 160, 0),
            "34": (148, 0, 211, 0),
            "35": (211, 211, 211, 0),
            "36": (107, 142, 35, 0),
            "37": (245, 245, 220, 0),
            "38": (132, 112, 255, 0),
            "39": (148, 0, 211, 0),
            "40": (112, 128, 144, 0),
            "41": (123, 104, 238, 0),
            "42": (211, 211, 211, 0),
            "43": (147, 112, 219, 0),
            "44": (50, 205, 50, 0),
            "45": (255, 239, 213, 0),
            "46": (105, 105, 105, 0),
            "47": (124, 252, 0, 0),
            "48": (143, 188, 143, 0),
            "49": (64, 224, 208, 0),
            "50": (160, 32, 240, 0),
            "51": (0, 250, 154, 0),
            "52": (208, 32, 144, 0),
            "53": (188, 143, 143, 0),
            "54": (143, 188, 143, 0),
            "55": (47, 79, 79, 0),
            "56": (0, 191, 255, 0),
            "57": (224, 255, 255, 0),
            "58": (135, 206, 235, 0),
            "59": (250, 240, 230, 0),
            "60": (245, 255, 250, 0),
            "61": (184, 134, 11, 0),
            "62": (240, 255, 255, 0),
            "63": (248, 248, 255, 0),
            "64": (208, 32, 144, 0),
            "65": (255, 140, 0, 0),
            "66": (85, 107, 47, 0),
            "67": (176, 196, 222, 0),
            "68": (106, 90, 205, 0),
            "69": (173, 255, 47, 0),
            "70": (132, 112, 255, 0),
            "71": (221, 160, 221, 0),
            "72": (205, 133, 63, 0),
            "73": (255, 99, 71, 0),
            "74": (199, 21, 133, 0),
            "75": (255, 165, 0, 0),
            "76": (255, 255, 255, 0),
            "77": (244, 164, 96, 0),
            "78": (95, 158, 160, 0),
            "79": (30, 144, 255, 0),
            "80": (102, 205, 170, 0),
            "81": (85, 107, 47, 0),
            "82": (189, 183, 107, 0),
            "83": (25, 25, 112, 0),
            "84": (147, 112, 219, 0),
            "85": (255, 250, 205, 0),
            "86": (255, 250, 240, 0),
            "87": (153, 50, 204, 0),
            "88": (173, 255, 47, 0),
            "89": (152, 251, 152, 0),
            "90": (255, 69, 0, 0),
            "91": (173, 216, 230, 0),
            "92": (238, 232, 170, 0),
            "93": (222, 184, 135, 0),
            "94": (224, 255, 255, 0),
            "95": (100, 149, 237, 0),
            "96": (250, 235, 215, 0),
            "97": (175, 238, 238, 0),
            "98": (255, 192, 203, 0),
            "99": (255, 240, 245, 0),
            "100": (160, 82, 45, 0),
            "101": (189, 183, 107, 0),
            "102": (119, 136, 153, 0),
            "103": (255, 222, 173, 0),
            "104": (238, 221, 130, 0),
            "105": (100, 149, 237, 0),
            "106": (0, 0, 128, 0),
            "107": (176, 196, 222, 0),
            "108": (0, 100, 0, 0),
            "109": (60, 179, 113, 0),
            "110": (186, 85, 211, 0),
            "111": (32, 178, 170, 0),
            "112": (176, 224, 230, 0),
            "113": (255, 255, 0, 0),
            "114": (250, 235, 215, 0),
            "115": (127, 255, 212, 0),
            "116": (253, 245, 230, 0),
            "117": (175, 238, 238, 0),
            "118": (0, 250, 154, 0),
            "119": (219, 112, 147, 0),
            "120": (138, 43, 226, 0),
            "121": (218, 112, 214, 0),
            "122": (190, 190, 190, 0),
            "123": (72, 61, 139, 0),
            "124": (107, 142, 35, 0),
            "125": (188, 143, 143, 0),
            "126": (34, 139, 34, 0),
            "127": (0, 255, 127, 0),
            "128": (244, 164, 96, 0),
            "129": (34, 139, 34, 0),
            "130": (245, 245, 245, 0),
            "131": (210, 105, 30, 0),
            "132": (233, 150, 122, 0),
            "133": (106, 90, 205, 0),
            "134": (255, 105, 180, 0),
            "135": (112, 128, 144, 0),
            "136": (255, 105, 180, 0),
            "137": (255, 0, 0, 0),
            "138": (176, 224, 230, 0),
            "139": (238, 221, 130, 0),
            "140": (105, 105, 105, 0),
            "141": (47, 79, 79, 0),
            "142": (240, 128, 128, 0),
            "143": (238, 232, 170, 0),
            "144": (245, 245, 245, 0),
            "145": (255, 228, 196, 0),
            "146": (0, 191, 255, 0),
            "147": (176, 48, 96, 0),
            "148": (255, 228, 225, 0),
            "149": (60, 179, 113, 0),
            "150": (210, 180, 140, 0),
            "151": (152, 251, 152, 0),
            "152": (199, 21, 133, 0),
            "153": (255, 245, 238, 0),
            "154": (255, 222, 173, 0),
            "155": (0, 0, 205, 0),
            "156": (46, 139, 87, 0),
            "157": (139, 69, 19, 0),
            "158": (240, 128, 128, 0),
            "159": (119, 136, 153, 0),
            "160": (240, 230, 140, 0),
            "161": (255, 228, 225, 0),
            "162": (255, 239, 213, 0),
            "163": (238, 130, 238, 0),
            "164": (240, 255, 240, 0),
            "165": (0, 206, 209, 0),
            "166": (205, 92, 92, 0),
            "167": (255, 255, 224, 0),
            "168": (0, 255, 255, 0),
            "169": (25, 25, 112, 0),
            "170": (186, 85, 211, 0),
            "171": (255, 218, 185, 0),
            "172": (139, 69, 19, 0),
            "173": (255, 20, 147, 0),
            "174": (255, 160, 122, 0),
            "175": (255, 218, 185, 0),
            "176": (211, 211, 211, 0),
            "177": (0, 0, 0, 0),
            "178": (253, 245, 230, 0),
            "179": (255, 248, 220, 0),
            "180": (255, 255, 240, 0),
            "181": (250, 128, 114, 0),
            "182": (65, 105, 225, 0),
            "183": (32, 178, 170, 0),
            "184": (30, 144, 255, 0),
            "185": (255, 160, 122, 0),
            "186": (0, 0, 128, 0),
            "187": (245, 255, 250, 0),
            "188": (135, 206, 235, 0),
            "189": (153, 50, 204, 0),
            "190": (255, 215, 0, 0),
            "191": (255, 250, 250, 0),
            "192": (135, 206, 250, 0),
            "193": (255, 182, 193, 0),
            "194": (0, 255, 0, 0),
            "195": (165, 42, 42, 0),
            "196": (105, 105, 105, 0),
            "197": (135, 206, 250, 0),
            "198": (216, 191, 216, 0),
            "199": (255, 250, 240, 0),
            "200": (255, 235, 205, 0),
            "201": (211, 211, 211, 0),
            "202": (119, 136, 153, 0),
            "203": (255, 255, 224, 0),
            "204": (255, 235, 205, 0),
            "205": (124, 252, 0, 0),
            "206": (255, 127, 80, 0),
            "207": (250, 250, 210, 0),
            "208": (255, 182, 193, 0),
            "209": (70, 130, 180, 0),
            "210": (47, 79, 79, 0),
            "211": (255, 69, 0, 0),
            "212": (184, 134, 11, 0),
            "213": (112, 128, 144, 0),
            "214": (70, 130, 180, 0),
            "215": (119, 136, 153, 0),
            "216": (218, 165, 32, 0),
            "217": (47, 79, 79, 0),
            "218": (72, 209, 204, 0),
            "219": (255, 250, 205, 0),
            "220": (0, 206, 209, 0),
            "221": (72, 61, 139, 0),
            "222": (102, 205, 170, 0),
            "223": (220, 220, 220, 0),
        }

        self.colours_default = dict(self.colours)

        # replace colours with CA-specififc aliases
        if aliases:
            for key in aliases.keys():
                self.colours[key] = aliases[key]

        self.missing_col = (220,220,220,0)

    # Returns a color based on an input integer i.e. cell state
    def getColour(self, intcolour):
        if not self.colours.get(str(intcolour)):
            return self.missing_col
        else:
            return self.colours.get(str(intcolour))

    def get_default_Colour(self, intcolour):
        if not self.colours_default.get(str(intcolour)):
            return self.missing_col
        else:
            return self.colours_default.get(str(intcolour))
