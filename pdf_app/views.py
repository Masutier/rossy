import json
import os
from django.contrib import messages
from django.shortcuts import render, redirect
from PyPDF2 import PdfFileReader, PdfFileWriter, PdfReader
from .utils import *

destiny_path = "/home/gabriel/Documents/catalogRossy/destiny/"
origen_path = "/home/gabriel/Downloads/"
endDir = ""


def pdfTool(request):
    catalogList = []
    path = (destiny_path)
    chkFolder = os.path.isdir(path)
    if not chkFolder:
        messages.info(request, 'El archivo no existe')
        return redirect('/pdfLoad')
    else:
        catalogList = os.listdir(path)
        catalogList.sort()
        context = {"title": "pdf", 'catalogList': catalogList, 'abs_path':path}
        return render(request, 'pdf_app/pdfTool.html', context)


def pdfLoad(request):
    count = 0
    count1 = 0
    count2 = 50
    count3 = 100
    count4 = 150
    count5 = 200
    count6 = 250
    firstcount = 0
    secondcount = 0
    thirdcount = 0
    fourthcount = 0
    fifthcount = 0
    sixthcount = 0
    catalogList = []

    if request.method == 'POST':
        pdfFile = request.FILES['inputPdf']
        user_answer = request.POST['exampleRadios']
        month = request.POST['mes']
        nameFile = pdfFile.name
        fileNamex = nameFile.split('.')
        file_tp_pross = origen_path + nameFile
        global endDir

        if user_answer == "Compu":
            endDir = crearFolder(destiny_path, fileNamex, month)

            #OPEN FILE
            with open(file_tp_pross, "rb") as f:
                reader = PdfFileReader(f)

                part1 = PdfFileWriter()
                first = list(range(0, 51))

                part2 = PdfFileWriter()
                second = list(range(50, 101))

                part3 = PdfFileWriter()
                third = list(range(100, 151))

                part4 = PdfFileWriter()
                fourth = list(range(150, 201))

                part5 = PdfFileWriter()
                fifth = list(range(200, 251))
                
                part6 = PdfFileWriter()
                sixth = list(range(250, 301))

                for page in range(len(reader.pages)):
                    if page in first:
                        count1 += 1
                        part1.addPage(reader.getPage(page))
                        firstcount = 1

                    if page in second:
                        count2 += 1
                        part2.addPage(reader.getPage(page))
                        secondcount = 1

                    if page in third:
                        count3 += 1
                        part3.addPage(reader.getPage(page))
                        thirdcount = 1

                    if page in fourth:
                        count4 += 1
                        part4.addPage(reader.getPage(page))
                        fourthcount = 1
                    
                    if page in fifth:
                        count5 += 1
                        part5.addPage(reader.getPage(page))
                        fifthcount = 1

                    if page in sixth:
                        count6 += 1
                        part6.addPage(reader.getPage(page))
                        sixthcount = 1

                pieceOut = destiny_path + fileNamex[0] + "_" + month + "/" + fileNamex[0]

                if firstcount == 1:
                    piece = origen_path + "/" + fileNamex[0] + "_part1.pdf"
                    with open(piece, "wb") as f2:
                        part1.write(f2)
                    count = 0
                    imagensAll(count, piece, pieceOut)

                if secondcount == 1:
                    piece = origen_path + "/" + fileNamex[0] + "_part2.pdf"
                    with open(piece, "wb") as f3:
                        part2.write(f3)
                    count = 50
                    imagensAll(count, piece, pieceOut)

                if thirdcount == 1:
                    piece = origen_path + "/" + fileNamex[0] + "_part3.pdf"
                    with open(piece, "wb") as f4:
                        part3.write(f4)
                    count = 100
                    imagensAll(count, piece, pieceOut)

                if fourthcount == 1:
                    piece = origen_path + "/" + fileNamex[0] + "_part4.pdf"
                    with open(piece, "wb") as f5:
                        part4.write(f5)
                    count = 150
                    imagensAll(count, piece, pieceOut)

                if fifthcount == 1:
                    piece = origen_path + "/" + fileNamex[0] + "_part5.pdf"
                    with open(piece, "wb") as f6:
                        part5.write(f6)
                    count = 200
                    imagensAll(count, piece, pieceOut)

                if sixthcount == 1:
                    piece = origen_path + "/" + fileNamex[0] + "_part6.pdf"
                    with open(piece, "wb") as f6:
                        part6.write(f6)
                    count = 250
                    imagensAll(count, piece, pieceOut)

            return redirect('/pdfTool')

    return render(request, 'pdf_app/pdfLoad.html')


def pdfExport(request):
    catalogList = []
    cat = ""
    path = (destiny_path)
    chkFolder = os.path.isdir(path)

    if not chkFolder:
        messages.info(request, 'El archivo no existe')
        return redirect('/pdfLoad')
    else:
        catalogList = os.listdir(path)
        catalogList.sort()

    if request.method == 'POST':
        data = request.POST.get("cat")
        print("data", data)
        for cat in catalogList:
            if data == cat:
                print("**********", data)
            else:
                print(cat)

        context = {"title": "xxx", 'data':data}
        return render(request, 'pdf_app/xxx.html', context)

    context = {"title": "showup", 'path':path, 'catalogList': catalogList}
    return render(request, 'pdf_app/showup.html', context)


def xxx(request):

    return render(request, 'pdf_app/xxx.html', context)
