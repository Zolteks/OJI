class Tools:
    def center(x, y, w, h, w2, h2):
        x_o = x + w/2 - w2/2
        y_o = y + h/2 - h2/2
        return x_o, y_o

    def normalizeTriggerVal(v):
        return v/32767

    def normalizeStickVal(v):
        return (v + 32768)/65535