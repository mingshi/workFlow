# -*- coding: utf-8 -*-
'''
Author  :   Mingshi <fivemingshi@gmail.com>
Created :   2014/03/11 14:55:40
FileName:   BaseWFConfig.py
'''

'''
第一版的流程控制
由于流程相对较简单，而且人员不是很多，所以直接在配置文件中写死
'''

WORK_FLOW = {
        '1' : { 
            'uid' : ['flow_uid', 1, 11, 1, 1],
            'des' : ['申请者填写测试时间段', '财务付款', '测试负责人审批', 'CEO终审', '关闭'],
            'can' : ['create', 'finance', 'testadmin', 'ceo', 'closer']
        },

        '2' : {
            'uid' : [1, 11, 1, 1],
            'des' : ['财务审核', '流量运营专员', '合同管理专员', '关闭'],
            'can' : ['finance', 'trafficadmin', 'contractadmin', 'closer']
        },

        '3' : {
            'uid' : [11, 18, 1, 18],
            'des' : ['运营数据', '财务审核', 'CEO审核', '财务付款', '关闭'],
            'can' : ['traffic', 'finance', 'ceo', 'finance', 'closer']
        },

        '4' : {
            'uid' : [11, 1, 18, 1],
            'des' : ['财务审核', 'ceo审核', '合同专员审核', '关闭'],
            'can' : ['finance', 'ceo', 'contractadmin', 'closer']
        }
}
