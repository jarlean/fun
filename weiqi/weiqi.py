#-*-coding:utf-8-*-

import random

class Upgrade:
    '''
        计算围棋晋级率
        调用示例：
            请输入参赛人数:100
            请输入比赛场次:7
            请输入晋级场次:5
    '''

    def __init__(self,count,vote_cnt,score_up,score_down):
        '''
        初始化参赛人数
        :param self:
        :param count:参赛人数
        :param vote_cnt:比赛场次
        :param score_up:晋级场次
        :param score_down:失败场次
        :param player_upg:晋级选手，{编号:[当前分数,[对手,分数]]}
        :param player_fail:淘汰选手，{编号:[当前分数,[对手,分数]]}
        :param player:参赛人员，{编号:[当前分数,[对手,分数]]}
        :param pscore:比赛成绩，[编号:胜利场次]
        :return:
        '''
        self.player= {}
        self.pscore= []
        self.player_upg= {}
        self.player_fail= {}
        self.vote_cnt = vote_cnt
        self.score_up = score_up
        self.score_up = score_up
        self.score_down = score_down
        for i in range(count):
            # 初始化参赛选手名单
            self.pscore.append([i,0])
            self.player[self.pscore[i][0]] = self.player.get(self.pscore[i][0], [self.pscore[i][1], []])
        # print('参赛人数:{},参数人员信息{}'.format(count,self.player))

    def sort(self,pscore):
        '''
        对比赛结果排序
        :param player:
        :return:
        '''
        pscore.sort(key=lambda kv:kv[1],reverse=True)
        return pscore

    def pk(self,playerid1,playerid2):
        '''
        比赛，并返回比赛结果
        :return:
        '''
        scoreone=random.choice([0,1])
        if scoreone == 0:
            for i in range(len(self.pscore)):
                if self.pscore[i][0]==playerid1:
                    # print('参赛选手%s成绩+0'%playerid1)
                    self.pscore[i][1] += 0
                elif self.pscore[i][0]==playerid2:
                    # print('参赛选手%s成绩+1'%playerid2)
                    self.pscore[i][1] += 1
        elif scoreone == 1:
            for i in range(len(self.pscore)):
                if self.pscore[i][0]==playerid1:
                    # print('参赛选手%s成绩+1'%playerid1)
                    self.pscore[i][1] += 1
                elif self.pscore[i][0]==playerid2:
                    # print('参赛选手%s成绩+0'%playerid2)
                    self.pscore[i][1] += 0


        # return [self.pscore]

    def update_player(self,playerid1,playerid2=''):
        # 根据比赛成绩，修改选手信息
        # 选手的编号，与self.pscore[0]相等时，代表同一个选手
        # print('更新选手信息前：选手1：%s:%s，选手2：%s:%s'%(playerid1,self.player.get(playerid1), playerid2,self.player.get(playerid2)))
        for player in self.pscore:
            # 更新选手1成绩及对手信息
            if int(player[0]) == playerid1:
                # 更新成绩
                self.player[playerid1][0] = player[1]
                # 记录比赛对手信息
                if playerid2=='':
                    self.player[playerid1][1]=self.player[playerid1][1]+[['', 0]]
                else:
                    self.player[playerid2][1]=self.player[playerid2][1]+[[player[0], player[1]]]
            # 更新选手2成绩及对手信息
            elif int(player[0]) == playerid2:
                # 更新成绩
                self.player[playerid2][0] = player[1]
                self.player[playerid2][1]=self.player[playerid2][1]+[[player[0], player[1]]]
            else:
                continue
        # print('更新选手信息后：选手1：%s:%s，选手2：%s:%s'%(playerid1,self.player.get(playerid1), playerid2,self.player.get(playerid2)))

    def pop_player(self,votecur):
        # 例如 7局5胜晋级，7局3负淘汰
        # 例如 7局4胜晋级，7局4负淘汰
        # 选手晋级或淘汰(当前胜场 >= 升级场次) or (当前负场 >= 失败场次)
        # print('晋级场次%s，淘汰场次%s'%(self.score_up,self.score_down))
        flag=True
        for i in range(len(self.pscore)):
        # while flag:
        #     if len(self.pscore)<=0:
        #         flag=False
            # 对所有选手进行升级、淘汰
            # 当选手升级、淘汰，则弹出，并重新开始获取选手清单
            for ps in self.pscore:
                # 第3场
                suc = ps[1] # 0
                fail = votecur - ps[1] # 3 - 0 = 3
                # print('选手比赛成绩：%s，胜利次数%s，失败次数%s'%(ps,suc,fail))
                # 晋级、淘汰选手弹出
                if suc >= self.score_up or fail >= self.score_down:
                    if suc >= self.score_up:
                        # 成功选手赋值给player_upg
                        self.player_upg[ps[0]] = self.player.get(ps[0])
                        # 晋级与失败是互斥事件，要用elif
                    elif fail >= self.score_down:
                        # 成功选手赋值给player_fail
                        self.player_fail[ps[0]] = self.player.get(ps[0])
                    for i in range(len(self.pscore)):
                        # 选手达到升级分数，找出升级的选手，并弹出，退出循环继续寻找下一个晋级选手
                        if self.pscore[i][0] == ps[0]:
                            self.pscore.pop(i)
                            break




if __name__=='__main__':
    '''
    1级升1段，7局4胜晋级，分数8分晋级
    分数达到8，则不再比赛
      当前分数 = 8
    分数无法达到8，则不再比赛
      7*2 - 当前场次*2 - 当前分数 < 8
    '''
    # 初始化参赛人数
    # count=12
    count=int(input('请输入参赛人数:'))
    # 初始化比赛场次
    # votecnt=7
    vote_cnt=int(input('请输入比赛场次:'))
    # 初始化晋级场次
    # voteup=4
    score_up=int(input('请输入晋级场次:'))
    # 当前场次
    votecur=0
    # 计算淘汰场次
    score_down=vote_cnt-score_up+1

    upg = Upgrade(count,vote_cnt,score_up,score_down)


    for p in range(vote_cnt):
        votecur += 1
        # print('-' * 200)
        # print('第%s轮比赛编排:%s' % (votecur, upg.pscore))

        # 第一轮比赛
        if len(upg.pscore) % 2 == 1:
            upg.pscore[len(upg.pscore)-1][1]+=1
            # 记录选手对手及成绩
            upg.update_player(upg.pscore[len(upg.pscore)-1][0])
            for i in range(0,len(upg.pscore)-1,2):
                # 比赛选手编号为：upg.pscore[i][0]，upg.pscore[i+1][0]
                # print('当前参赛选手%s-----%s'%(upg.pscore[i][0],upg.pscore[i+1][0]))
                upg.pk(upg.pscore[i][0],upg.pscore[i+1][0])
                # 记录选手对手及成绩
                upg.update_player(upg.pscore[i][0],upg.pscore[i+1][0])

        else:
            for i in range(0,len(upg.pscore),2):
                # 比赛并更新成绩
                upg.pk(upg.pscore[i][0],upg.pscore[i+1][0])
                # 记录选手对手及成绩
                upg.update_player(upg.pscore[i][0],upg.pscore[i+1][0])


        # 选手信息更新后，将晋级、淘汰选手剔除
        upg.pop_player(votecur)

        upg.sort(upg.pscore)

        # print('第%s场比赛后，选手信息：%s'%(p+1,upg.player))
        # print('第%s场比赛后，晋级选手信息：%s'%(p+1,upg.player_upg))
        # print('第%s场比赛后，失败选手信息：%s'%(p+1,upg.player_fail))
        # print('第%s场比赛后，选手成绩：%s'%(p+1,upg.pscore))

    print('*'*100)
    print('第%s场比赛后，晋级选手编号：%s'%(p+1,upg.player_upg.keys()))
    print('第%s场比赛后，失败选手编号：%s'%(p+1,upg.player_fail.keys()))
    print('*'*100)
    print('本次比赛参与人数{}，晋级人数{}，未晋级人数{}，晋级率{}%'.format(count,len(upg.player_upg),len(upg.player_fail),round(len(upg.player_upg)*100/count,2)))
    print('*'*100)
