from pprint import pprint

from django.shortcuts import render
import os
import pandas as pd
import glob
import pathlib
import xml.etree.ElementTree as ET




def preview(request,current_directory='./',sub_directory='media/'):
    current_directory
    # pprint(request.param['subfolder'])
    print("current_directory: "+current_directory)
    print("sub_directory: "+sub_directory)
    print(current_directory+sub_directory)
    img_folder=sub_directory
    # フォルダ情報
    # p = pathlib.Path(current_directory+sub_directory)
    p = pathlib.Path('./media')
    print(p)
    sub_directories = []
    for x in p.iterdir():
        if x.is_dir():
            sub_directories.append(str(x).replace('media\\', ''))

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
        # print(p.name)
        # print(type(p.name))
        # print(p)
        DateTimeFile = p.name.split(None, 1)
        # print(DateTimeFile[1])
        DateTimeFile[1] = DateTimeFile[1].replace('_src.png', '')
        # print(DateTimeFile[1])
        DateTimeFile.append(p.name)
        # print(DateTimeFile)
        list_png_DTF.append(DateTimeFile)
    # print(list_png_DTF)
    df_png = pd.DataFrame(list_png_DTF,
                          columns=['DATE', 'TIME', 'FILE NAME'])
    # print(df_png)
    ############################################################
    #
    # XML に関する処理：
    # -- 検知に関するXMLファイルの読み込みとdf_pngとの突合
    # -- df_xmlにもDTF情報は含まれるが、XMLの内容も含まれるようにする
    #
    ############################################################
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
        #
        # print(root)
        # print(root.attrib)
        # print(node.attrib)
        # lprint(node)

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
            DTF.append(image)
            DTF.append(rect)
            DTF.append(level)
            DTF.append(p19)
            DTF.append(size)
            ###
            ###
            ###
            # print(DTF)
            list_xml_DTF.append(DTF)
    ######
    # print(DateTimeFile)

    ######
    # print(list_xml_DTF)
    df_xml = pd.DataFrame(list_xml_DTF,
                          columns=['DATE', 'TIME', 'IMAGE', 'RECT', 'LEVEL', 'P19', 'SIZE'])
    df_xml["IMAGE"] = df_xml["IMAGE"].map(lambda s: "<img src='"+img_folder+"{}' width='200' />".format(s))
    context={
        'sub_directories':sub_directories,
        'preview_df' : df_xml.to_html(escape=False),
    }

    ###
    ### REF
    ###
    # -- https://maku77.github.io/python/parse-xml-by-element-tree.html
    # -- https://docs.python.org/ja/3/library/xml.etree.elementtree.html?highlight=find
    # -- https://www.digifie.jp/blog/archives/1459
    ###
    ###
    ###

    ############################################################
    # l
    # HTML上に出力するためのdf_PNGとdf_XMLの突合処理・配列成形処理：
    #
    ############################################################

    ############################################################
    #
    # HTMLへの出力処理＜１＞基本出力
    # ・表形式へのHTMLレンダリング
    # ・ファイル名へのhref処理／リンクはローカルpath
    # ・https://qiita.com/nshinya/items/a46ef0002284d2f77789
    # ・https://di-acc2.com/programming/python/5322/
    #
    ############################################################
    ############################################################
    #
    # HTMLへの出力処理＜２＞成形処理
    # ・検知ファイルの月別、週別表示用のHTML生成
    # ・統計情報の表示
    # ・HELPや問い合わせ
    #
    ############################################################

    return render(request,"preview.html",context)







def previewsubfolder(request,subfolder='media'):
    print(subfolder)
    img_folder='media/'
    #フォルダ情報
    p = pathlib.Path('./media')
    sub_folders = []
    for x in p.iterdir() :
        if x.is_dir():
            sub_folders.append(str(x).replace('media\\',''))


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
        # print(p.name)
        # print(type(p.name))
        # print(p)
        DateTimeFile = p.name.split(None, 1)
        # print(DateTimeFile[1])
        DateTimeFile[1] = DateTimeFile[1].replace('_src.png', '')
        # print(DateTimeFile[1])
        DateTimeFile.append(p.name)
        # print(DateTimeFile)
        list_png_DTF.append(DateTimeFile)
    # print(list_png_DTF)
    df_png = pd.DataFrame(list_png_DTF,
                          columns=['DATE', 'TIME', 'FILE NAME'])
    # print(df_png)
    ############################################################
    #
    # XML に関する処理：
    # -- 検知に関するXMLファイルの読み込みとdf_pngとの突合
    # -- df_xmlにもDTF情報は含まれるが、XMLの内容も含まれるようにする
    #
    ############################################################
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
        #
        # print(root)
        # print(root.attrib)
        # print(node.attrib)
        # lprint(node)

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
            DTF.append(image)
            DTF.append(rect)
            DTF.append(level)
            DTF.append(p19)
            DTF.append(size)
            ###
            ###
            ###
            # print(DTF)
            list_xml_DTF.append(DTF)
    ######
    # print(DateTimeFile)

    ######
    # print(list_xml_DTF)
    df_xml = pd.DataFrame(list_xml_DTF,
                          columns=['DATE', 'TIME', 'IMAGE', 'RECT', 'LEVEL', 'P19', 'SIZE'])
    df_xml["IMAGE"] = df_xml["IMAGE"].map(lambda s: "<img src='"+img_folder+"{}' width='200' />".format(s))
    context={
        'sub_folders':sub_folders,
        'preview_df' : df_xml.to_html(escape=False),
    }

    ###
    ### REF
    ###
    # -- https://maku77.github.io/python/parse-xml-by-element-tree.html
    # -- https://docs.python.org/ja/3/library/xml.etree.elementtree.html?highlight=find
    # -- https://www.digifie.jp/blog/archives/1459
    ###
    ###
    ###

    ############################################################
    # l
    # HTML上に出力するためのdf_PNGとdf_XMLの突合処理・配列成形処理：
    #
    ############################################################

    ############################################################
    #
    # HTMLへの出力処理＜１＞基本出力
    # ・表形式へのHTMLレンダリング
    # ・ファイル名へのhref処理／リンクはローカルpath
    # ・https://qiita.com/nshinya/items/a46ef0002284d2f77789
    # ・https://di-acc2.com/programming/python/5322/
    #
    ############################################################
    ############################################################
    #
    # HTMLへの出力処理＜２＞成形処理
    # ・検知ファイルの月別、週別表示用のHTML生成
    # ・統計情報の表示
    # ・HELPや問い合わせ
    #
    ############################################################

    return render(request,"preview.html",context)
