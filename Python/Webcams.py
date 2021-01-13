import cv2


def ScanWebcam(*args):
    for X in range(*args):
        cap = cv2.VideoCapture(X, cv2.CAP_DSHOW)
        if cap.isOpened():
            for Z in range(10):
                cv2.waitKey(5)
                _, img = cap.read()
                cv2.imshow("Cam ID:"+str(X), img)
            print("ID: [" + str(X) + "] disponível")
        else:
            print("ID: [" + str(X) + "] Inválido")


def OpenWebcam(ID, **kargs):
    cap = cv2.VideoCapture(ID, cv2.CAP_DSHOW)
    Pfx = kargs.get('Prefix')
    Sfx = kargs.get('Sufix')
    path = kargs.get('Save')
    imgName = kargs.get('ImgName')
    idn = ' [ID: ' + str(ID) + '] '
    tecla = kargs.get('Trigger')
    if Sfx or Pfx:
        if Pfx and Sfx:
            name = (str(Pfx) + idn + str(Sfx))
        elif not Sfx:
            name = (str(Pfx) + idn)
        else:
            name = (idn + str(Sfx))
    else:
        name = idn
    if path:
        print("Aperte "+ tecla +" para salvar em "+str(path))
    if cap.isOpened():
        while True:
            _, img = cap.read()

            cv2.imshow(name, img)
            key = cv2.waitKey(1)
            try:
                print(ord(key))
            except TypeError:
                pass
            if key == 27:
                cv2.destroyAllWindows()
                break
            elif key == ord(tecla):
                cv2.imwrite('../Master/Imagens/Teste/'+str(imgName)+'.jpg', img)




# ScanWebcam(3)
OpenWebcam(0, Prefix='Camera:', Sufix='...', Save='../Master/Imagens/Teste', ImgName='CameraA', Trigger='S')

