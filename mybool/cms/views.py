from pprint import pprint

from django.shortcuts import render
import os
import pandas as pd
import glob
import pathlib
import xml.etree.ElementTree as ET




def preview(request):
    base_dir='./media'
    current_directory = request.GET.get('current_directory')
    select_directory=request.GET.get('sub_directory')
    if current_directory is None:
        current_directory = './media'
    print("curren_directory: "+current_directory)
    if select_directory is None:
        new_current_directory=current_directory
    else:
        select_directory=request.GET.get('sub_directory')
        new_current_directory = current_directory + '/' + select_directory
        new_current_directory=current_directory+'/'+select_directory
    # pprint(request.param['subfolder'])
    print("newcurrent_directory: "+new_current_directory)
    img_folder=new_current_directory+'/'
    print("img_folder: "+img_folder)
    # フォルダ情報
    # p = pathlib.Path(current_directory+sub_directory)
    p = pathlib.Path(new_current_directory)
    print(p)
    sub_directories = []
    for x in p.iterdir():
        if x.is_dir():
            sub_directories.append(str(x).replace('media\\', ''))
            # sub_directories.append(str(x))

    print(sub_directories)
    # ^[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]_[0-9][0-9]_[0-9][0-9]_src\.png$

    ##################
    ##################
    # 　https://www.one-tab.com/page/VM_CZ7siSA6gOszVhIaqgA
    # 　https://www.one-tab.com/page/dWaxd76jR3G9MOYBwlBOBw
    ##################
    ##################

    # Directory Change
    # os.chdir('logs')
    # globで指定するのでいらない
    # globにはglobの特殊文字があり正規表現とは異なるので注意

    df = pd.DataFrame(columns=[])
    # test

    ############################################################
    #
    # PNG に関する処理：
    # -- 検知ファイルの日付、時間、ファイル名の配列化処理
    #
    ############################################################
    RegEx1 = '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]_[0-9][0-9]_[0-9][0-9]_src.png'
    p_temp = pathlib.Path(img_folder).glob(RegEx1)
    count = 0
    # 各種ファイル処理
    list_png_DTF = []
    # list_png_DTF.append(['DATE','TIME','FILE NAME'])
    # print(list_png_DTF)
    for p in p_temp:

        DateTimeFile = p.name.split(None, 1)
        DateTimeFile.append(p.name)
        list_png_DTF.append(DateTimeFile)
    df_png = pd.DataFrame(list_png_DTF,
                          columns=['DATE', 'TIME', 'FILE NAME'])

    RegEx2 = '[0-9][0-9][0-9][0-9]-[0-9][0-9]-[0-9][0-9] [0-9][0-9]_[0-9][0-9]_[0-9][0-9]_img.xml'
    p_temp2 = pathlib.Path(img_folder).glob(RegEx2)
    count = 0
    # 各種ファイル処理
    list_xml_DTF = []
    for p2 in p_temp2:
        DateTimeFile = p2.name.split(None, 1)
        ##
        DateTimeFile[1] = DateTimeFile[1].replace('_img.xml', '')
        # DateTimeFile.append(p2.name)
        ##
        xml_tree = ET.parse(img_folder + p2.name)
        root = xml_tree.getroot()
        node = root.findall('face')
        #
        # findall() は、リストを返してしまうので注意
        # find だと face が複数あった時最初のfaceしか返さない


        count = 0
        for nd in node:
            DTF = []
            DTF.extend(DateTimeFile)
            count = +1
            # print(nd.attrib)
            ###

            # ROW.append(DateTimeFile)
            # print(ROW[count-1])
            ###
            image=p2.name.replace('_img.xml', '_src.png')
            rect = nd.get('face_rect')
            level = nd.get('level')
            p19 = nd.get('p19')
            size = nd.get('img_size')
            DTF.append(rect)
            DTF.append(level)
            DTF.append(p19)
            DTF.append(size)
            DTF.append(image)

            list_xml_DTF.append(DTF)

    df_xml = pd.DataFrame(list_xml_DTF,
                          columns=['DATE', 'TIME', 'RECT', 'LEVEL', 'P19', 'SIZE', 'IMAGE'])
    df_xml["IMAGE"] = df_xml["IMAGE"].map(lambda s: "<img src='"+img_folder+"{}' width='200' />".format(s))
    context={
        'current_directory':current_directory,
        'sub_directories':sub_directories,
        'preview_df' : df_xml.to_html(escape=False),
    }


    return render(request,"preview.html",context)
