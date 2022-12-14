from copy import deepcopy
from func_timeout import FunctionTimedOut, func_timeout
import random
import board
import sys
import math

from math import log, sqrt

class Node:
    def __init__(self, board, parent, color, action):
        self.parent = parent # 父节点
        self.children = [] # 子节点列表
        self.visit_times = 0 # 访问次数
        self.board = board # 游戏选择这个Node的时的棋盘
        self.color = color # 当前玩家
        self.prevAction = action # 到达这个节点的action
        self.unvisitActions = list(board.get_legal_actions(color)) # 未访问过的actions
        self.isover = self.gameover(board) # 是否结束了
        if (self.isover == False) and (len(self.unvisitActions) == 0): # 没得走了但游戏还没结束
            self.unvisitActions.append("noway")
        
        self.reward = {'X': 0, 'O': 0}
        self.bestVal = {'X': 0, 'O': 0}
    
    def gameover(self, board):
        l1 = list(board.get_legal_actions('X'))
        l2 = list(board.get_legal_actions('O'))
        return len(l1)==0 and len(l2)==0
    
    def calcBestVal(self, balance, color):
        if self.visit_times==0:
            print("-------------------------")
            print("oops!visit_times==0!")
            self.board.display()
            print("-------------------------")
        self.bestVal[color] = self.reward[color] / self.visit_times + balance * sqrt(2 * log(self.parent.visit_times) / self.visit_times)

class MonteCarlo:
    # uct方法的实现
    # return: action(string)
    def search(self, board, color):
        # board: 当前棋局
        # color: 当前玩家
        
        # 特殊情况：只有一种选择
        actions=list(board.get_legal_actions(color))
        if len(actions) == 1:
            return list(actions)[0]
        
        # 创建根节点
        newboard = deepcopy(board)
        root = Node(newboard, None, color, None)
        
        # 考虑时间限制
        try:
            # 测试程序规定每一步在60s以内
            func_timeout(59, self.whileFunc, args=[root])
        except FunctionTimedOut:
            pass
            
    return self.best_child(root, math.sqrt(2), color).prevAction


    def whileFunc(self, root):
        while True:
            # mcts four steps
            # selection,expantion
            expand_node = self.tree_policy(root)
            # simulation
            reward = self.default_policy(expand_node.board, expand_node.color)
            # Backpropagation
            self.backup(expand_node, reward)

def expand(self, node):
    """
        输入一个节点，在该节点上拓展一个新的节点，使用random方法执行Action，返回新增的节点
        """
            
            action = random.choice(node.unvisitActions)
            node.unvisitActions.remove(action)
            
            # 执行action，得到新的board
            newBoard = deepcopy(node.board)
            if action != "noway":
                newBoard._move(action, node.color)
                    else:
                        pass
                            
                            newColor = 'X' if node.color=='O' else 'O'
                                newNode = Node(newBoard,node,newColor,action)
                                node.children.append(newNode)
                                
                                    return newNode

def best_child(self, node, balance, color):
    # 对每个子节点调用一次计算bestValue
    for child in node.children:
        child.calcBestVal(balance, color)
        
        # 对子节点按照bestValue排序，降序
        sortedChildren = sorted(node.children, key=lambda x: x.bestVal[color], reverse = True)
        
        # 返回bestValue最大的元素
        return sortedChildren[0]
    
    def tree_policy(self, node):
        """
            传入当前需要开始搜索的节点（例如根节点）
            根据exploration/exploitation算法返回最好的需要expend的节点
            注意如果节点是叶子结点直接返回。
            """
        retNode = node
        while not retNode.isover:
            if len(retNode.unvisitActions)>0:
                # 还有未展开的节点
                return self.expand(retNode)
            else:
                # 选择val最大的
                retNode = self.best_child(retNode, math.sqrt(2), retNode.color)
    
    return retNode

def default_policy(self, board, color):
    """
        蒙特卡罗树搜索的Simulation阶段
        输入一个需要expand的节点，随机操作后创建新的节点，返回新增节点的reward。
        注意输入的节点应该不是子节点，而且是有未执行的Action可以expend的。
        
        基本策略是随机选择Action。
        """
            newBoard = deepcopy(board)
            newColor = color
                
                def gameover(board):
                    l1 = list(board.get_legal_actions('X'))
                    l2 = list(board.get_legal_actions('O'))
                    return len(l1)==0 and len(l2)==0
                        
                        while not gameover(newBoard):
                            actions = list(newBoard.get_legal_actions(newColor))
                            if len(actions) == 0:
                                action = None
                                    else:
                                        action = random.choice(actions)
                                            
                                            if action is None:
                                                pass
                                                    else:
                                                        newBoard._move(action, newColor)
                                                            
                                                            newColor = 'X' if newColor=='O' else 'O'
                                                                
                                                                # 0黑 1白 2平局
                                                                winner, diff = newBoard.get_winner()
                                                                diff /= 64
                                                                    return winner, diff

def backup(self, node, reward):
    newNode = node
        # 节点不为None时
        while newNode is not None:
            newNode.visit_times += 1
            
            if reward[0] == 0:
                newNode.reward['X'] += reward[1]
                newNode.reward['O'] -= reward[1]
            elif reward[0] == 1:
                newNode.reward['X'] -= reward[1]
                newNode.reward['O'] += reward[1]
            elif reward[0] == 2:
                pass
            
            newNode = newNode.parent




class AIPlayer:
    """
    AI 玩家
    """

    def __init__(self, color):
        """
        玩家初始化
        :param color: 下棋方，'X' - 黑棋，'O' - 白棋
        """

        self.color = color

    def get_move(self, board):
        """
        根据当前棋盘状态获取最佳落子位置
        :param board: 棋盘
        :return: action 最佳落子位置, e.g. 'A1'
        """
        if self.color == 'X':
            player_name = '黑棋'
        else:
            player_name = '白棋'
        print("请等一会，对方 {}-{} 正在思考中...".format(player_name, self.color))

        # -----------------请实现你的算法代码--------------------------------------

        mcts = MonteCarlo()
        action = mcts.search(board, self.color)
        # action = UCT_Search.UCTSearch(board, self.color)
        # ------------------------------------------------------------------------

        return action
