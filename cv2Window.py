import cv2
class Window():
    def __init__(self, name, var_list, var_range, new_win = False,  w_width = None, w_height=None, default_value = None, func_list = None):
        self.name = name
        self.var_list = var_list
        self.var_range = var_range
        self.func_list = func_list

        if len(var_list) != len(var_range):
            print("ERROR: Worng variable name and range not match!")
            pass

        if new_win:
            cv2.namedWindow(name, cv2.WINDOW_GUI_NORMAL)   
            if w_width or w_height:
                cv2.resizeWindow(name, w_width, w_height)

        for i in range(len(var_list)):
            moving = self.func_list[i] if self.func_list else lambda x : x
            cv2.createTrackbar(var_list[i], name, var_range[i][0], var_range[i][1], moving)

            if default_value:
                if default_value[i] <var_range[i][0] or default_value[i] > var_range[i][1]:
                    print("Default out of bound")
                    pass

                cv2.setTrackbarPos(var_list[i], name, default_value[i])

    def getAllTrackbarPos(self):
        res = []
        for var in self.var_list:
            res.append(cv2.getTrackbarPos(var, self.name))
        return res
    

