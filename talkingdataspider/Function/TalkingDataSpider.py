from selenium import webdriver
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.wait import WebDriverWait
from PIL import Image
import time
import os
import re
import platform
def PythonLocation():
	return os.path.dirname(os.path.realpath(__file__))
def CurrentPlatform():
	sysstr = platform.system()
	if(sysstr =="Windows"):
		return "Windows"
	elif(sysstr == "Linux"):
		return "Linux"
	elif(sysstr == "Darwin"):
		return "Mac"
	else:
		return "None"
class TDSpider:
	#Channel Param Start
	ChannelName = "TD"
	# UserName = 'tool@east2west.cn'
	UserName = '3rd@east2west.cn'
	password = 'hello123456'
	LoginPostLink = 'https://account.talkingdata.com/?backurl=https://www.talkingdata.com&languagetype=zh_cn'
	#Channel Param End
	def __init__(self,CompanyName):
		#获取此公司名的账户密码
		#GetAccount(self,CompanyName)

		if CurrentPlatform()=="Mac":
			self.driver=webdriver.Safari()
		else:
			self.driver=webdriver.Firefox()
		self.driver.get(self.LoginPostLink)
		wait=WebDriverWait(self.driver,10)
		input_email=self.driver.find_element_by_id('email')
		input_password=self.driver.find_element_by_id('password')
		input_email.send_keys(self.UserName)
		input_password.send_keys(self.password)
		self.driver.find_element_by_id('btn-normal-login').click()
		# button=wait.until(EC.element_to_be_clickable((By.CLASS_NAME,'login-operate')))
		# time.sleep(1)
		# button.click()
		print("登陆成功")
		time.sleep(1)
	def TDSpider_Revenue(self):
		self.driver.get('https://www.talkingdata.com/product-game.jsp?languagetype=zh_cn')
		time.sleep(2)#浏览器响应
		tag_url = self.driver.find_element_by_class_name('pro-operates').find_elements_by_tag_name('a')[0].get_attribute('href')
		self.driver.get(tag_url)
		time.sleep(3)#浏览器响应
		trList = self.driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
		nTr = len(trList)
		for n in range(nTr):
			tdList = trList[n].find_elements_by_tag_name("td")
			div = tdList[0].find_elements_by_tag_name("div")[3]
			if "集成中" not in div.text and "Integrating" not in div.text:
				print(tdList[0].find_element_by_tag_name("a").get_attribute("title"))
				# trello上任务：每个游戏的新增用户（游戏列表>新增账户）
				print(tdList[2].find_element_by_tag_name("h4").text)

				tdList[5].find_elements_by_tag_name("a")[1].click()
				time.sleep(3)#浏览器响应
				#新增用户
				print("[新增用户]	",self.driver.find_element_by_id("totalNewPlayerNum").text)
				#总启动次数
				#总时长
				#新增付费用户
				print("[总付费用户数]	",self.driver.find_element_by_id("totalChargePlayerNum").text)
				#活跃用户
				self.driver.find_element_by_class_name("Players").click()
				time.sleep(1.5)#等待js渲染
				self.driver.find_element_by_xpath('//a[@url-data="player-active"]').click()
				time.sleep(1.5)#等待js渲染
				print("[日活跃用户数]	",self.driver.find_element_by_id("dauAvg").find_element_by_tag_name("em").text)
				#总付费用户
				#总付费金额
				#总用户
				#广告展示率
				#广告点击率
				#留存率
				#计费点展示率
				#计费点点击率
				#LTV



				"""--->游戏习惯"""
				self.driver.find_element_by_xpath('//a[@url-data="player-behavior"]').click()
				time.sleep(5)#等待js渲染
				print("游戏平均时长:",self.driver.find_element_by_xpath('//span[@id="avgTimeAndTimeCode-avg"]').find_elements_by_tag_name('em')[1].text)
				"""--->推广渠道--->渠道数据"""
				self.driver.find_element_by_class_name('partnerExtention').click()
				time.sleep(1.5)#等待js渲染
				self.driver.find_element_by_xpath('//a[@url-data="partnerExtention-partnerData"]').click()
				time.sleep(6)#等待js渲染
				trList = self.driver.find_element_by_xpath('//tbody[@data="amount"]').find_elements_by_tag_name('tr')
				for tr in trList:
					tdList = tr.find_elements_by_tag_name('td')
					if tdList[0].text != "":
						print("渠道名:",tdList[0].text,"  玩家注册数:",tdList[3].text)
				
				"""--->自定义事件--->事件数据"""
				#只拿这两个数据的详细内容(DisplayAD HitAD)
				self.driver.find_element_by_class_name('CustomEvent').click()
				time.sleep(1.5)#等待js渲染
				self.driver.find_element_by_xpath('//a[@url-data="customEvent-data"]').click()
				time.sleep(6)#等待js渲染
				trList = self.driver.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
				nTr = len(trList)
				for n in range(nTr):
					tdList = trList[n].find_elements_by_tag_name("td")
					if "DisplayAD" in tdList[0].text or "HitAD" in tdList[0].text:
						print(tdList[0].text,"  弹出次数:",tdList[1].text,"  点击次数:",tdList[2].text)
						tdList[0].find_element_by_tag_name("a").click()
						time.sleep(6)#等待js渲染
						ctrList = self.driver.find_element_by_id("paramsTable").find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
						try:
							for nctr in range(len(ctrList)):
								strong = ctrList[nctr].find_element_by_tag_name("td").find_element_by_tag_name("strong")
								strong.click()
								time.sleep(2)
								tables = self.driver.find_element_by_id("paramsTable").find_elements_by_xpath('//table[@class="table_style1"]')[-1].find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")
								print(strong.text)
								for ctb in tables:
									ctdList = ctb.find_elements_by_tag_name("td")
									for ctd in ctdList:
										print(ctd.text,end="    ")
									print()
						except:
							print("该游戏未接入自定义事件")

						self.driver.find_element_by_xpath('//a[@url-data="customEvent-data"]').click()
						time.sleep(6)#等待js渲染
						trList = self.driver.find_element_by_tag_name("tbody").find_elements_by_tag_name("tr")


				print("测试")

				self.driver.get(tag_url)
				time.sleep(6)#浏览器响应
				trList = self.driver.find_element_by_tag_name('tbody').find_elements_by_tag_name('tr')
		self.strs = re.search("<([\s\S]*)>",self.driver.page_source).group()
		time.sleep(10)
		# print(self.strs)
		self.driver.close()
	def SaveContext(self):
		if os.path.exists(PythonLocation()+"\\Revenue")==False:
			os.mkdir(PythonLocation()+"\\Revenue")
		# with open(PythonLocation()+"\\Revenue\\"+self.ChannelName+".json", 'w') as out:
		# 	json.dump(self._TD_dict, out, ensure_ascii=False)#ensure_ascii=False 以中文形式输入
		with open(PythonLocation()+"\\Revenue\\"+self.ChannelName+".html", 'w',encoding='utf-8') as out:
			out.write(self.strs)
	def GetAccount(self,CompanyName):
		#获取账户Configuration/Account.json
		pass

def main():
	CompanyName="E2W"
	TD = TDSpider(CompanyName)
	TD.TDSpider_Revenue()
	TD.SaveContext()
if __name__ == '__main__':
	main()
