#-*-coding:utf-8-*-
import pandas as pd

pf1 = pd.read_csv('0854最多翻4页.csv')
pf1.to_excel('0854最多翻4页.xlsx', sheet_name='data')