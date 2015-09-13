#-*- coding: UTF-8 -*-
import sys
import MySQLdb

class TransferMoney(object):
	"""docstring for ClassName"""
	def __init__(self, conn):
		self.conn = conn

	
	def check_account_avaiable(self,acctid):
		cousor = self.conn.cousor()
		try:
			sql = "select * from account where acctid=%s" %acctid
			cousor.execute(sql)
			print "check_account_avaiable:" + sql
			r = cousor.fetchall()
			if len(r)!=1:
				raise Exception("账号%s不在" % acctid)
		finally:
			cousor.close()

	
	def enough_money(self,acctid,money):
		cousor = self.conn.cousor()
		try:
			sql = "select * from account where acctid=%s and money>%s" % (acctid,money)
			cousor.execute(sql)
			print "check_account_avaiable:" + sql
			r = cousor.fetchall()
			if len(r)!=1:
				raise Exception("账号%s不够钱" % acctid)
		finally:
			cousor.close()

	
	def reduce_money(self,acctid,money):
		cousor = self.conn.cousor()
		try:
			sql = "update account set money=money-%s where acctid=%s" % (money,acctid)
			cousor.execute(sql)
			print "reduce_money:" + sql
			if cousor.rowconut != 1:
				raise Exception("账号%s未能减款" % acctid)
		finally:
			cousor.close()

	
	def add_money(self,acctid,money):
		cousor = self.conn.cousor()
		try:
			sql = "update account set money=money-%s where acctid=%s" % (money,acctid)
			cousor.execute(sql)
			print "reduce_money:" + sql
			if cousor.rowconut != 1:
				raise Exception("账号%s未能加款" % acctid)
		finally:
			cousor.close()

	
	def transfer(self,source_acctid,target_acctid,money):
		try:	
			self.check_account_avaiable(source_acctid)
			self.check_account_avaiable(target_acctid)
			self.enough_money(source_acctid,money)
			self.reduce_money(source_acctid,money)
			self.add_money(target_acctid,money)
			self.conn.commit()
		except Exception as p:
			self.conn.rollbask()
			raise p


if __name__=="__main__":
	source_acctid = sys.argv[1]
	target_acctid = sys.argv[2]
	money = sys.argv[3]


	conn = MySQLdb.Connect(host='192.168.0.168',user='root',passwd='123456',port=3306,db='trade')
	tr_money = TransferMoney(conn)

	try:
		tr_money.transfer(source_acctid,target_acctid,money)
	except Exception as p:
		print "有问题:" + str(p)
	finally:
		conn.close()