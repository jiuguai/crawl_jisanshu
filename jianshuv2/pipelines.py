from scrapy.exceptions import DropItem
import pymysql
from jianshuv2.items import Jianshuv2Item

class JanShuPipeline2:
	def __init__(self):
		self.sql= """
		INSERT INTO jst_pg(title, publish_time, author, content, words_count, page_url, user_profile, comments_count, likes_count, views_count,special_id) VALUES ( %(title)s, %(publish_time)s, %(author)s, %(content)s, %(words_count)s, %(page_url)s, %(user_profile)s, %(comments_count)s, %(likes_count)s, %(views_count)s,%(special_id)s);
		"""
		self.update_sql = """
			UPDATE jst_pg set special=%(special)s WHERE special_id=%(special_id)s
		"""

		self.con = pymysql.connect(host='localhost',user="root",password="root",database='jianshu',port=3306)
	def open_spider(self,spider):	
		self.cursor = self.con.cursor()

	def process_item(self,item,spider):
		if isinstance(item, Jianshuv2Item):
			try:
				self.cursor.execute(self.sql,dict(item))
				self.con.commit()
			except Exception as e:
				print('='*30,'出错了')
				print(item['page_url'])
				print(e)
				raise DropItem(item['page_url'])
		else:
			try:
				self.cursor.execute(self.update_sql,dict(item))
				self.con.commit()
			except Exception as e:
				print('='*30,'出错了')
				print(item['page_url'])
				print(e)
				raise DropItem(item['page_url'])
		return item

	def close_spider(self,spider):
		self.con.close()



class JanShuPipeline:
	def __init__(self):
		self.sql= """
		INSERT INTO jst_pg(title, publish_time, author, content, words_count, page_url, user_profile, comments_count, likes_count, views_count,special_id,special) VALUES ( %(title)s, %(publish_time)s, %(author)s, %(content)s, %(words_count)s, %(page_url)s, %(user_profile)s, %(comments_count)s, %(likes_count)s, %(views_count)s,%(special_id)s,%(special)s);
		"""
		self.con = pymysql.connect(host='localhost',user="root",password="root",database='jianshu',port=3306)
	def open_spider(self,spider):
		
		self.cursor = self.con.cursor()


	def process_item(self,item,spider):
		try:
			self.cursor.execute(self.sql,dict(item))
			self.con.commit()
		except Exception as e:
			print('='*30,'出错了')
			print(item['page_url'])
			print(e)
			raise DropItem(item['page_url'])
		return item

	def close_spider(self,spider):
		self.con.close()


