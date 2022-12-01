import os
from io import BytesIO
from pdf2image import convert_from_bytes
from pydrive.auth import GoogleAuth
from pydrive.drive import GoogleDrive

destiny_path = "/home/gabriel/Downloads/catalogRossy/destiny/"
origen_path = "/home/gabriel/Downloads/catalogRossy/"


def crearFolder(destiny_path, fileNamex, month):
    os.makedirs(destiny_path + fileNamex[0] + "_" + month)
    endDir = destiny_path + fileNamex[0] + "_" + month
    return endDir


def goDrive(catalog, catalogList):
    gauth = GoogleAuth()
    gauth.LoadClientConfigFile('settings.yaml')
    gauth.LocalWebserverAuth()
    drive = GoogleDrive(gauth)
    count = 0
    for upload_file in catalogList:
        count += 1
        gfile = drive.CreateFile({'parents': [{'id': catalog}]})
        gfile.SetContentFile(upload_file)
        gfile.Upload()
    gfile.content.close()
    return


def imagensAll(count, piece, pieceOut):
    images = convert_from_bytes(open(piece, 'rb').read())
    for imag in images:
        count += 1
        if imag.width > 1000:
            new_img = (1000, None)
            imag.save(pieceOut + "_" + str(count) + '.jpg', 'JPEG', quality=95)
        else:
            imag.save(pieceOut + "_" + str(count) + '.jpg', 'JPEG', quality=95)
    return
