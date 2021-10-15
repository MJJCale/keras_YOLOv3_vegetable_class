def convert_bbox(a):
    '''实现归一化bbox的逆运算'''
    #a是一个列表，其格式是 归一化中心x 归一化中心y 归一化bbox宽 归一化bbox高
    #归一化之后的格式  xmin ymin xmax ymax
    a[1] = float(a[1])
    a[2] = float(a[2])
    a[3] = float(a[3])
    a[4] = float(a[4])
    
    image_width = 1280
    image_height = 720

    dw = 1/image_width
    dh = 1/image_height
    x = a[1] / dw
    y = a[2] / dh
    w = a[3] / dw
    h = a[4] / dh
    xmin = int(x - (1/2)*w)
    ymin = int(y - (1/2)*h)
    xmax = int(y + (1/2)*h)
    ymax = int(x + (1/2)*w)
    return xmin,ymin,xmax,ymax
