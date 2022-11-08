# -*- coding: utf-8 -*-
import sys,json,os
from urllib import parse
from django.shortcuts import render,HttpResponse,redirect
from django.http import StreamingHttpResponse
sys.path.insert(0,sys.path[0] + "/../pirategamefinder/StartSearch")
import SinglaSearch
SABCD = ["S","A","B","C","D","TBD"]
undata_time = 0
def	ListFolder(path):
	List = []
	for i in os.listdir(path):
		List.append(i)
	return List
def InquireJsonLocation(Location,key):
	fileList = ListFolder(Location)
	global undata_time
	fileLocation = ""
	for file in fileList:
		if key in file and undata_time<=int(file.replace(key,"").replace("_","")):
			undata_time = int(file.replace(key,"").replace("_",""))
			fileLocation = file
	print(undata_time,fileLocation)
	return Location + "/" + fileLocation
JsonLocation = InquireJsonLocation(sys.path[0] + "/cache/E2W/AppMonitor","A") + "/results.json"
# Create your views here.
def UndataTime():
	global undata_time
	undata = str(undata_time)[:4] + "年" + str(undata_time)[4:6] + "月" + str(undata_time)[6:8] + "日" + str(undata_time)[8:10] + "点" + str(undata_time)[10:12] + "分" + str(undata_time)[12:] + "秒"
	return undata
def down_file(file_name, file_size = 512):
	with open(file_name,"rb") as f:
		while True:
			a = f.read(file_size)
			if a:
				yield a
			else:
				break
def PirateGameSearch(request, key):#get访问
	k = parse.unquote(key)
	if "GamePublishList" in k:
		"""
		response = StreamingHttpResponse("../pirategamefinder/StartSearch/GamePublishList.xlsx")
		response['Content-Type']='application/octet-stream'
		response['Content-Disposition']='attachment;filename="GamePublishList.xlsx"'
		return response
		"""
		ExcelLocation = InquireJsonLocation(sys.path[0] + "/cache/E2W/AppMonitor","A") + "/GamePublishList.xlsx"
		file=open(ExcelLocation,"rb")
		response =HttpResponse(file)
		response['Content-Type']='application/octet-stream'
		response['Content-Disposition']='attachment;filename="GamePublishList.xlsx"'
		return response

	print("游戏查询中...")
	global JsonLocation
	f = open(sys.path[1] + "/templates/PirateGameSearch.html",'r',encoding='utf-8')
	s = f.read()
	if "StartSearch" in k:
		k = k.replace("StartSearch","")
		mkPath = SinglaSearch.SinglaSearch(k)
		JsonLocation = sys.path[0] + "/cache/E2W/AppMonitor/" + mkPath + "/results.json"
	elif "WebImage" in k:
		k = k.replace("StartSearch","")
		print("待展示图片")
		JsonLocation = InquireJsonLocation(sys.path[0] + "/cache/E2W/AppMonitor","A") + "/results.json"
	else:
		JsonLocation = InquireJsonLocation(sys.path[0] + "/cache/E2W/AppMonitor","A") + "/results.json"
	s = s.replace("{{ option }}",AnalysisJsonOption()).replace("{{ table }}",AnalysisJson(k)).replace("{{ undata }}",UndataTime())
	print("游戏查询成功！！！")
	return HttpResponse(s)#render做渲染
# def MyTable(request):#post访问
# 	f = open(sys.path[1] + "/templates/MyTable.html",'r',encoding='utf-8')
# 	s = f.read()
# 	s = s.replace("{{ option }}",AnalysisJsonOption())
# 	if request.method == "POST":
# 		s = s.replace("{{ table }}",AnalysisJson(request.POST.get('key')))
# 	else:
# 		s = s.replace("{{ table }}",'')
# 	return HttpResponse(s)#render做渲染
def AnalysisJsonOption():
	result = json.load(open(JsonLocation,'r',encoding='utf-8'))
	Option_str = ''
	for key in result.keys():
		if key not in SABCD:
			Option_str = Option_str + '<option value="' + key + '">' + key + '</option>'
	return Option_str
def AnalysisJson(keys):
	result = json.load(open(JsonLocation,'r',encoding='utf-8'))
	Game_str = ''
	for key in result.keys():
		if key not in SABCD and key == keys:
			for n in range(0,len(result.get(key)),2):
				Game_str = Game_str + '<tr><th align="center">' + key + '</th>  <th align="center" width="35%">' + result[key][n] + '</th>'
				if  "_App" in result[key][n] and 'http' in result[key][n+1]:
					Game_str = Game_str + '<th align="center" width="25%"><a href="javascript:void(0);" onclick="ShowApp(\'' + result[key][n].replace("_App","") + '\',\''+ result[key][n+1] + '\')">链接</a>'
					# Game_str = Game_str + '<th align="center" width="25%"><a href="javascript:void(0);" onclick="ShowApp(\'' + result[key][n].replace("_App","") + '\',\''+ result[key][n+1] + '\')">链接</a>&nbsp;&nbsp;<a href="javascript:void(0);" onclick="ShowImage(\'' + key + '\',\''+ result[key][n] + '\')">图片</a></th></tr>'
				elif 'http' in result[key][n+1] and 'post' not in result[key][n+1]:
					Game_str = Game_str + '<th align="center" width="25%"><a href="' + result[key][n+1] + '" target="_blank" >链接</a>'
					# Game_str = Game_str + '<th align="center" width="25%"><a href="' + result[key][n+1] + '" target="_blank" >链接</a>&nbsp;&nbsp;<a href="javascript:void(0);" onclick="ShowImage(\'' + key + '\',\''+ result[key][n] + '\')">图片</a></th></tr>'
					# Game_str = Game_str + '<th align="center" width="25%"><a href="' + result[key][n+1] + '" target="_blank" >链接</a>&nbsp;&nbsp;<a href="/WebImage' + key + result[key][n] + '" target="_blank" >图片</a></th></tr>'
				else:
					Game_str = Game_str + '<th align="center" width="25%">未找到链接</th></tr>'
	return Game_str
"""
def AnalysisJson():
	result = json.load(open(JsonLocation,'r',encoding='utf-8'))
	Game_str = ''
	for key in result.keys():
		if key not in SABCD:
			for n in range(0,len(result.get(key)),2):
				Game_str = Game_str + '<tr><th align="center">' + key + '</th>  <th align="center">' + result[key][n] + '</th>'
				if 'http' in result[key][n+1] and 'post' not in result[key][n+1]:
					Game_str = Game_str + '<th align="center"><a href="' + result[key][n+1] + '">查看</a></th></tr>'
				else:
					Game_str = Game_str + '<th align="center">无盗版游戏</th></tr>'
	return Game_str
# """