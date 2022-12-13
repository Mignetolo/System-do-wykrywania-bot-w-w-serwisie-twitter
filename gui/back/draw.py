from diagrams import Diagram,Node
from diagrams.custom import Custom
from .get_data import get_follow
from .user_model import  user_prediction_explain
import os
import matplotlib.pyplot as plt
import networkx as nx

def checkifbot(id,user_model, text_model,):
    if user_prediction_explain(id, user_model, text_model, False) == 1:
       str = "../front/bot.png"
    else :
       str = "../front/human.png"
    print(str)
    return str 
        

def d_diagram(id, who,user_model, text_model):
    if f"{who}.png" not in os.listdir("gui/temp"): 
        list_json = get_follow(id, who)
        list = []
        for item in list_json:
            list.append([item["username"], item["id"]])
        with Diagram("",show=False, filename=f"gui/temp/{who}", direction="LR"):
            center = Custom( "you", checkifbot(id,user_model, text_model))
            for item in list[:4]:
                try :
                    kuston = Node(item[0], image=checkifbot(item[1],user_model, text_model),penwidth="1.0")
                    center >> kuston
                except:
                    pass
    return f"gui/temp/{who}.png"

def networkx_draw(id, who,user_model, text_model):
    G=nx.Graph()
    if f"{who}.png" not in os.listdir("gui/temp"): 
        list_json = get_follow(id, who)
        list = []
        for item in list_json:
            list.append([item["username"], item["id"]])
        print(list)
        for item in list[:4]:
            #try:
            if user_prediction_explain(id, user_model, text_model, False) == 1:
                G.add_node(f"{item[0]}",color = "red",style='filled')
                print("1")
            else :
                G.add_node(f"{item[0]}",color = "green",style='filled')
                print("2")
            #except:
                #pass
    pos = nx.circular_layout(G)
    nx.draw(G,pos=pos,node_size=1500,)
    #plt.tight_layout()
   # plt.show(block=False)
    plt.savefig("Graph.png", format="PNG")