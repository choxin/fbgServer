# -*- coding: utf-8 -*-
import ErrorCode
import TimerDefine
import util
from KBEDebug import DEBUG_MSG
import lotteryConfig

__author__ = 'chongxin'

Lottery_Type_Gold = 1
Lottery_Type_Diamond = 2
Lottery_Type_Ten = 3

class LotteryModule:
    def __init__(self):
        pass

    def onEntitiesEnabled(self):
        rebateTime = lotteryConfig.baseConfig[1]["resetTime"]
        offset = util.getLeftSecsToNextHMS(rebateTime,0,0)
        self.addTimer(offset, 24 * 60 * 60, TimerDefine.Timer_reset_lottery_free_times)

    # --------------------------------------------------------------------------------------------
    #                              客户端调用函数
    # --------------------------------------------------------------------------------------------
    def onClientLottery(self,lotteryType):

        DEBUG_MSG("lotteryType:--------------------------------" + str(lotteryType))
        if lotteryType not in lotteryConfig.lottery.keys():
            DEBUG_MSG("---------------dont have key")
            return

        lonfig = lotteryConfig.lottery[lotteryType]
        if lotteryType == Lottery_Type_Gold:
            result = self.goldLottery(lonfig)
        elif lotteryType == Lottery_Type_Diamond:
            result = self.diamondLottery(lonfig)
        elif lotteryType == Lottery_Type_Ten:
            result = self.tenLottery(lonfig)
        DEBUG_MSG("lotteryResult:-----" + str(result[0])+"----------------------" + str(result[1]))
        self.client.lotteryResult(result[0],result[1])


    # --------------------------------------------------------------------------------------------
    #                              工具函数调用函数
    # --------------------------------------------------------------------------------------------
    # 钞票抽
    def goldLottery(self,configDict):
        result =""
        op = ErrorCode.LotteryError.Success
        # 检查冷却时间
        # 检查免费次数
        #

        cdTime = configDict["cdTime"]
        moneyCount = configDict["moneyCount"]
        dropIds = configDict["dropIds"]

        lastTime = self.goldLastTime
        nowTime = util.getCurrentTime()
        period = nowTime - lastTime


        isUseGold = True
        if period >= cdTime and  self.goldFreeTimes >0:
            isUseGold = False

        if isUseGold :
            if self.gold >= moneyCount:
                self.gold = self.gold - moneyCount
            else:
                return (ErrorCode.LotteryError.Money_not_enough,"")
        else:
            self.goldFreeTimes = self.goldFreeTimes - 1

        self.goldLastTime = nowTime

        for key in dropIds:
            result += str(key) + ","

        DEBUG_MSG("goldLottery----------" + result)
        return (op,result)

    # 钻石抽卡
    def diamondLottery(self,configDict):
        result = ""
        op = ErrorCode.LotteryError.Success
        # 检查冷却时间
        # 检查免费次数
        #

        cdTime = configDict["cdTime"]
        moneyCount = configDict["moneyCount"]
        dropIds = configDict["dropIds"]

        lastTime = self.diamondLastTime
        nowTime = util.getCurrentTime()
        period = nowTime - lastTime

        isUseDiamond = True
        if period >= cdTime and self.diamondFreeTimes > 0:
            isUseDiamond = False

        if isUseDiamond:
            if self.diamond >= moneyCount:
                self.diamond = self.diamond - moneyCount
            else:
                return (ErrorCode.LotteryError.Diamond_not_enough, "")
        else:
            self.diamondFreeTimes = self.diamondFreeTimes - 1

        self.diamondLastTime = nowTime

        for key in dropIds:
            result += str(key) + ","

        DEBUG_MSG("diamondLottery ----------" + result)
        return (op, result)

    # 十连抽
    def tenLottery(self,configDict):
        result =""
        op = ErrorCode.LotteryError.Success

        moneyCount = configDict["moneyCount"]

        if self.diamond >= moneyCount:
            self.diamond = self.diamond - moneyCount
        else:
            return (ErrorCode.LotteryError.Diamond_not_enough, "")

        count = 10
        dropIds = configDict["dropIds"]
        tenDropIds = configDict["tenDropIds"]
        if self.tenFirstCall == 0:
            count = count -1
            for key in tenDropIds:
                result += str(key) + ","

            self.tenFirstCall = 1


        for i in range(count):
            for key in dropIds:
                result += str(key) + ","

        DEBUG_MSG("tenLottery ----------" + result)
        return (op, result)


    def onTimer(self, tid, userArg):
        if userArg != TimerDefine.Timer_reset_lottery_free_times:
            return

        config = lotteryConfig.lottery[Lottery_Type_Gold]

        self.goldFreeTimes = config["freeTime"]

        config = lotteryConfig.lottery[Lottery_Type_Diamond]

        self.diamondFreeTimes = config["freeTime"]

"""
    1、倒计时验证
    2、免费次数回复
"""



























