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
        }
}
