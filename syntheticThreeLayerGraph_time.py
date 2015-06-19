__author__ = "Moses A. Boudourides & Sergios T. Lenis"
__copyright__ = "Copyright (C) 2015 Moses A. Boudourides & Sergios T. Lenis"
__license__ = "Public Domain"
__version__ = "1.0"

'''
This script constructs a temporal random graph with 3 time slices.
'''

import networkx as nx
import matplotlib.pyplot as plt
from networkx.algorithms import bipartite
from matplotlib.patches import Ellipse, Polygon
import matplotlib
import itertools as it
from collections import Counter


def synthetic_three_level(n,p1,p2,p3,J_isolates=False,F_isolates=False,D_isolates=False):#,isolate_up=True,isolate_down=True):
    
    k=n

    J=nx.erdos_renyi_graph(n,p1) #The first layer graph
    Jis = nx.isolates(J)
    F=nx.erdos_renyi_graph(n,p2) #The second layer graph
    Fis = nx.isolates(F)
    D=nx.erdos_renyi_graph(n,p3) #The third layer graph
    Dis = nx.isolates(D)

    def translation_graph(J,F,D):
        H1=nx.Graph()
        H2=nx.Graph()
        for i in range(n):
            H1.add_edges_from([(J.nodes()[i],F.nodes()[i])])
            H2.add_edges_from([(F.nodes()[i],D.nodes()[i])])
        return H1, H2

    Jed = set(J.edges())
    Fed = set(F.edges())
    Ded = set(D.edges())
    l=[Jed,Fed,Ded]
    lu = list(set.union(*l))
    JFD=nx.Graph()
    JFD.add_edges_from(lu)

    G=nx.Graph()  #The synthetic two-layer graph
    
    # Relabing nodes maps
    
    mappingF={}
    for i in range(2*n):
        mappingF[i]=n+i
    FF=nx.relabel_nodes(F,mappingF,copy=True)
    
    mappingD={}
    for i in range(2*n):
        if i >n-1:
            mappingD[i]=i-n
        else:
            mappingD[i]=2*n+i
    DD=nx.relabel_nodes(D,mappingD,copy=True)
    
    H1, HH2 = translation_graph(J,FF,DD)
    
    G.add_edges_from(J.edges())
    G.add_edges_from(H1.edges())
    G.add_edges_from(DD.edges())
    G.add_edges_from(HH2.edges())
    G.add_edges_from(FF.edges())

    edgeList = []
    for e in H1.edges():
        edgeList.append(e)
    for e in HH2.edges():
        edgeList.append(e)
    
    return G, J, FF, DD, JFD, edgeList  


def plot_graph(n,G,J,FF,DD,JFD,d1=0.8,d2=5.0,nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):  
    
    if layout:
        pos=nx.spring_layout(JFD)
    else:
        pos=nx.random_layout(JFD)

    minPos=min(pos.keys())
    
    top_set=set()
    bottom_set=set()
    middle_set=set()
    level1=[]
    level2=[]
    level3=[]
    created_pos={}
    for j in range(3):
        for i in range(len(pos)):
            npos=pos[pos.keys()[i]]
            if j==0:
                ij=i
                created_pos[ij]=[d2*npos[0],d2*(npos[1]-d1)] 
                bottom_set.add(i)
                level3.append(created_pos[i])
            elif j==1:
                ij=i+n
                created_pos[ij]=[d2*(npos[0]),d2*(npos[1])] 
                middle_set.add(ij)
                level1.append(created_pos[ij])
            else:
                ij=i+2*n                
                created_pos[ij]=[d2*(npos[0]),d2*(npos[1]+d1)] 
                top_set.add(ij)
                level2.append(created_pos[ij])
    
    xlevel2=[i[0] for i in level2]
    ylevel2=[i[1] for i in level2]
    
    alevel2 = [min(xlevel2)-d1/2.-0.7,max(ylevel2)+d1/2.]
    blevel2 = [max(xlevel2)+d1/2.-0.7,max(ylevel2)+d1/2.]
    clevel2 = [max(xlevel2)+d1/2.,min(ylevel2)-d1/2.]
    dlevel2 = [min(xlevel2)-d1/2.,min(ylevel2)-d1/2.]

    xlevel3=[i[0] for i in level3]
    ylevel3=[i[1] for i in level3]

    alevel3 = [min(xlevel3)-d1/2.-0.7,max(ylevel3)+d1/2.]
    blevel3 = [max(xlevel3)+d1/2.-0.7,max(ylevel3)+d1/2.]
    clevel3 = [max(xlevel3)+d1/2.,min(ylevel3)-d1/2.]
    dlevel3 = [min(xlevel3)-d1/2.,min(ylevel3)-d1/2.]

    xlevel1=[i[0] for i in level1]
    ylevel1=[i[1] for i in level1]

    alevel1 = [min(xlevel1)-d1/2.-0.7,max(ylevel1)+d1/2.]
    blevel1 = [max(xlevel1)+d1/2.-0.7,max(ylevel1)+d1/2.]
    clevel1 = [max(xlevel1)+d1/2.,min(ylevel1)-d1/2.]
    dlevel1 = [min(xlevel1)-d1/2.,min(ylevel1)-d1/2.]

    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(111)

    ax.add_patch(Polygon([alevel2,blevel2,clevel2,dlevel2],color='b',alpha=0.1)) 
    plt.plot([alevel2[0],blevel2[0],clevel2[0],dlevel2[0],alevel2[0]],[alevel2[1],blevel2[1],clevel2[1],dlevel2[1],alevel2[1]],'-b')

    ax.add_patch(Polygon([alevel3,blevel3,clevel3,dlevel3],color='r',alpha=0.1)) 
    plt.plot([alevel3[0],blevel3[0],clevel3[0],dlevel3[0],alevel3[0]],[alevel3[1],blevel3[1],clevel3[1],dlevel3[1],alevel3[1]],'-r')

    ax.add_patch(Polygon([alevel1,blevel1,clevel1,dlevel1],color='g',alpha=0.1)) 
    plt.plot([alevel1[0],blevel1[0],clevel1[0],dlevel1[0],alevel1[0]],[alevel1[1],blevel1[1],clevel1[1],dlevel1[1],alevel1[1]],'-g')

    nx.draw(J,created_pos, with_labels=withlabels,nodelist=list(bottom_set),node_color='r',node_size=nodesize,edge_color='r',alpha=0.2)
    nx.draw(FF,created_pos, with_labels=withlabels,nodelist=list(middle_set),node_color='g',node_size=nodesize,edge_color='g',alpha=0.2)
    nx.draw(DD,created_pos, with_labels=withlabels,nodelist=list(top_set),node_color='b',node_size=nodesize,edge_color='b',alpha=0.2)
    nx.draw_networkx_edges(G,created_pos,edgelist=edgelist,edge_color='k',alpha=0.2)

    plt.show()

    return created_pos
def synthetic_multi_bipartite(k,n,m,p=[],No_isolates=True):

    # nx.bipartite_random_graph(n, m, p, seed=None, directed=False)
    list_of_Graphs=[]
    list_of_isolates=[]
    list_of_Graphs_final=[]
    for ij in range(k):
        while True:
            g=nx.bipartite_random_graph(n, m, p[ij])
            bipsets=bipartite.sets(g)
            if len(bipsets[0])==n and len(bipsets[1])==m:
                break
        # print len(bipsets[0]),len(bipsets[1])
        list_of_Graphs.append(g)#nx.bipartite_random_graph(n, m, p[ij]))
        # list_of_Graphs.append(nx.bipartite_gnmk_random_graph(n, m, p[ij]))
        list_of_isolates.append(nx.isolates(list_of_Graphs[ij]))

    Gagr=nx.Graph()
    for i in list_of_Graphs:
        Gagr.add_edges_from(i.edges())
        for nd in i.nodes(data=True):
            Gagr.add_node(nd[0],attr_dict=nd[1])
    # print Gagr.nodes()
    # print Gagr.edges()
    G=nx.Graph()  #The synthetic two-layer graph
    
    # Relabing nodes maps
    nm=n+m
    mapping={}
    for i in range(k):
        mapping[i]={}
        bisets=bipartite.sets(list_of_Graphs[i])
        # print bisets
        gh=nx.Graph()

        # for ij in range(nm):
        for ij in list_of_Graphs[i].nodes():
            coucou=ij+i*nm
            attrd=list_of_Graphs[i].node[ij]
            # if ij<n:
            # print ij,ij in bisets[0],coucou
            if ij in bisets[0]:
                mapping[i][ij]='A%i' %coucou
                gh.add_node('A%i' %coucou,attr_dict=attrd)
            else:
                mapping[i][ij]='B%i' %coucou
                gh.add_node('B%i' %coucou,attr_dict=attrd)
        # print i,gh.nodes()
        for ed in list_of_Graphs[i].edges():
            gh.add_edge(mapping[i][ed[0]],mapping[i][ed[1]])
        #     print ed
        #     print mapping[i][ed[0]],mapping[i][ed[1]]
        # print i,i,gh.nodes(data=True),bipartite.sets(gh)
        # print gh.edges()

        # list_of_Graphs_final.append(nx.relabel_nodes(list_of_Graphs[i],mapping[i],copy=True))
        list_of_Graphs_final.append(gh)
    list_of_translation_graphs=[]
    for ij in range(k-1):
        H1=nx.Graph()
        #### A small fix to pain in the ass
        g1=sorted(list_of_Graphs_final[ij].nodes())
        g2=sorted(list_of_Graphs_final[ij+1].nodes())
        #######
        # print '+++++++++++++++++++++'

        # print list_of_Graphs[ij].nodes(data=True),bipartite.sets(list_of_Graphs[ij])
        # print g1 ,bipartite.sets(list_of_Graphs_final[ij])
        # print list_of_Graphs_final[ij].nodes(data=True)

        # print [ik[0] for ik in list_of_Graphs_final[ij].nodes(data=True) if ik[1]['bipartite']==0]
        # print [ik[0] for ik in list_of_Graphs_final[ij].nodes(data=True) if ik[1]['bipartite']==1]
        # print mapping[ij]
        # # print g2,bipartite.sets(list_of_Graphs_final[ij+1])
        # print '=============='

        g1=list_of_Graphs_final[ij].nodes()
        g2=list_of_Graphs_final[ij+1].nodes()
        #######
        for ji in range(n+m):

            H1.add_edge(g1[ji],g2[ji]) #a small fix

        list_of_translation_graphs.append(H1)
    for i in list_of_Graphs_final:
        G.add_edges_from(i.edges())
        for nd in i.nodes(data=True):
            G.add_node(nd[0],attr_dict=nd[1])
        # G.add_nodes_from(i.nodes())
    # luf=set()
    # for i in list_of_Graphs_final:
    #     luf=luf.union(set(i.edges()))
    # luf=list(luf)
    # G.add_edges_from(luf)
    luf=set()
    for i in list_of_translation_graphs:

        luf=luf.union(set(i.edges()))
        G.add_edges_from(i.edges())
    # print G.nodes(data=True)   
    edgeList=list(luf)
    # G.add_edges_from(luf)
    nmap={}
    for i  in mapping:
        # print i,mapping[i]
        for j in mapping[i]:
            # print i,j,mapping[i][j]
            if j<n:
                nmap[mapping[i][j]]='A%i' %j
            else:
                nmap[mapping[i][j]]='B%i' %j

    return G, list_of_Graphs_final, Gagr, edgeList ,nmap ,mapping#F
def plot_graph_k_nm(k,n,m,G,list_of_Graphs_final, Gagr,d1=0,d2=2,d3=0,d4=.3,d5=1,d6=.4,d7=.2,d8=1,d9=0.3,colors_grey='gray',nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):  
    '''
    Plotting the synthetic graph after increasing the distance among layers by a parameter d1
    and dilating each layer by a parameter d1 
    '''
    # print k,n,G.nodes(),Gagr.nodes()
    if layout:
        pos=nx.spring_layout(Gagr)
    else:
        pos=nx.random_layout(Gagr)

    minPos=min(pos.keys())
    top_set=set()
    bottom_set=set()
    middle_set=set()
    levels=dict()
    created_pos={}
    if colors_grey=='gray':
        colors=['gray' for i in range (2*n)]

    elif colors_grey=='bipartite':
        colors=[]
        aset=[i[0] for i in G.nodes(data=True) if i[1]['bipartite']==0 ]
        bset=[i[0] for i in G.nodes(data=True) if i[1]['bipartite']==1 ]

        bipsets=(aset,bset)#bipartite.sets(G)
        for i in G.nodes():

            if i in bipsets[0]:
                colors.append('m')
            else:
                colors.append('g')
    else:
        colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]

    # bipsets=bipartite.sets(Gagr)
    # print bipsets
    # print aaa
    for j in range(k):
        aset=[i[0] for i in G.nodes(data=True) if i[1]['bipartite']==0 ]
        bset=[i[0] for i in G.nodes(data=True) if i[1]['bipartite']==1 ]

        bipsets=(aset,bset)#bipartite.sets(G)

        # bipsetsin=bipartite.sets(list_of_Graphs_final[j])
        aset=[i[0] for i in list_of_Graphs_final[j].nodes(data=True) if i[1]['bipartite']==0 ]
        bset=[i[0] for i in list_of_Graphs_final[j].nodes(data=True) if i[1]['bipartite']==1 ]
        bipsetsin=(aset,bset)
        # print bipsetsin

        sset=set()
        pos_lis=[]
        # for i in range(n):
        # print list_of_Graphs_final[j].nodes()
        col_li=[]
        for i,v in enumerate(list_of_Graphs_final[j].nodes()):
        # for i in range(n):
        # bipsetsin0=sorted(bipsetsin[0])
        # for i,v  in enumerate(bipsetsin0):
        # for i in range(nm):
            # ij=i+j*(n+m)
            # print i,v,j,ij

            npos=pos[i]


            created_pos[v]=[d2*npos[0],d8*(npos[1]+j*(n)*d6)] 
            sset.add(v)
            pos_lis.append(created_pos[v])
            # if v[0]=='A':
            if i<n:
            # if v in bipsets[0]:
                col_li.append('m')
            else:
                col_li.append('g')
            # col_li=colors[j]
            # if v in bipsets[0]:
            #     col_li.append('m')
            # else:
            #     col_li.append('g')]
        # bipsetsin1=sorted(bipsetsin[1])
        # for i,v  in enumerate(bipsetsin1):
        # # for i in range(nm):
        #     # ij=i+j*(n+m)
        #     # print i,v,j,ij

        #     npos=pos[i]


        #     created_pos[v]=[d2*npos[0],d8*(npos[1]+j*n*d6)] 
        #     sset.add(v)
        #     pos_lis.append(created_pos[v])
        #     col_li.append('g')

        levels[j]=(sset,pos_lis,col_li)
        # print levels[j]
        # print created_pos
    # print aaa
    xylevels={}

        # sset=set()
        # pos_lis=[]
        # for i in range(n):
        #     ij=i+j*n
        #     npos=pos[i]
        #     created_pos[ij]=[d2*npos[0],d8*(npos[1]+j*n*d6)] 
        #     sset.add(ij)
        #     pos_lis.append(created_pos[ij])
        #     col_li=colors[j]

        # levels[j]=(sset,pos_lis,col_li)

    xylevels={}

    for i in range(k):
        xlevel2=[ij[0] for ij in levels[i][1]]
        ylevel2=[ij[1] for ij in levels[i][1]]
        alevel2 = [min(xlevel2)-d1,max(ylevel2)+d7/2.-d3+d5]
        blevel2 = [max(xlevel2)+d9,max(ylevel2)+d7/2.+d3+d5]
        clevel2 = [max(xlevel2)+d9-d4,min(ylevel2)-d7/2.+d3-d5]
        dlevel2 = [min(xlevel2)-d1-d4,min(ylevel2)-d7/2.-d3-d5]
        xylevels[i]=[alevel2,blevel2,clevel2,dlevel2]


    fig=plt.figure(figsize=(10,10))
    ax=fig.add_subplot(111)
    for i in range(k):
        ax.add_patch(Polygon(xylevels[i],color='gray',alpha=0.1))
        xa=[j[0] for j in xylevels[i]]
        xa.append(xylevels[i][0][0])
        ya=[j[1] for j in xylevels[i]]
        ya.append(xylevels[i][0][1])
        plt.plot(xa,ya,'-',color='gray')
        nx.draw_networkx_nodes(list_of_Graphs_final[i],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.2)
        nx.draw_networkx_edges(list_of_Graphs_final[i],created_pos,alpha=0.2)
        # nx.draw(list_of_Graphs_final[i],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.2)
    # print edgelist
    # print G.nodes()
    # print created_pos

    nx.draw_networkx_edges(G,created_pos,edgelist=edgelist,edge_color='k',alpha=0.2)
    # for i in range(k):
    #     ax.add_patch(Polygon(xylevels[i],color=levels[i][2],alpha=0.1))
    #     xa=[j[0] for j in xylevels[i]]
    #     xa.append(xylevels[i][0][0])
    #     ya=[j[1] for j in xylevels[i]]
    #     ya.append(xylevels[i][0][1])
    #     plt.plot(xa,ya,'-',color=levels[i][2])

    #     nx.draw(list_of_Graphs_final[i],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.2)
    # # print edgelist
    # # print G.nodes()
    # nx.draw_networkx_edges(G,created_pos,edgelist=edgelist,edge_color='k',alpha=0.2)
    plt.axis('off')
    plt.show()

    return created_pos
def synthetic_multi_level(k,n,p=[],No_isolates=True):

    list_of_Graphs=[]
    list_of_isolates=[]
    list_of_Graphs_final=[]
    for ij in range(k):
        list_of_Graphs.append(nx.erdos_renyi_graph(n,p[ij]))
        list_of_isolates.append(nx.isolates(list_of_Graphs[ij]))

    Gagr=nx.Graph()
    for i in list_of_Graphs:
        Gagr.add_edges_from(i.edges())
        Gagr.add_nodes_from(i.nodes())

    G=nx.Graph()  #The synthetic two-layer graph
    
    # Relabing nodes maps
    mapping={}
    for i in range(k):
        mapping[i]={}
        for ij in range(n):
            mapping[i][ij]=ij+i*n

        list_of_Graphs_final.append(nx.relabel_nodes(list_of_Graphs[i],mapping[i],copy=True))

    list_of_translation_graphs=[]
    for ij in range(k-1):
        H1=nx.Graph()
        #### A small fix to pain in the ass
        g1=sorted(list_of_Graphs_final[ij].nodes())
        g2=sorted(list_of_Graphs_final[ij+1].nodes())
        #######

        for ji in range(n):

            H1.add_edge(g1[ji],g2[ji]) #a small fix

        list_of_translation_graphs.append(H1)

    luf=set()
    for i in list_of_Graphs_final:
        luf=luf.union(set(i.edges()))
    luf=list(luf)
    G.add_edges_from(luf)
    luf=set()
    for i in list_of_translation_graphs:
        luf=luf.union(set(i.edges()))
    edgeList=list(luf)
    G.add_edges_from(luf)
    nmap={}
    for i  in mapping:
        for j in mapping[i]:
            nmap[mapping[i][j]]=j

    return G, list_of_Graphs_final, Gagr, edgeList ,nmap ,mapping#F

def plot_graph_k(k,n,G,list_of_Graphs_final, Gagr,d1=0.8,d2=5.0,nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):  
    '''
    Plotting the synthetic graph after increasing the distance among layers by a parameter d1
    and dilating each layer by a parameter d1 
    '''

    if layout:
        pos=nx.spring_layout(Gagr)
    else:
        pos=nx.random_layout(Gagr)

    minPos=min(pos.keys())
    top_set=set()
    bottom_set=set()
    middle_set=set()
    levels=dict()
    created_pos={}
    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    for j in range(k):

        sset=set()
        pos_lis=[]
        for i in range(n):
            ij=i+j*n
            npos=pos[i]
            created_pos[ij]=[d2*npos[0],d2*(npos[1]+j*n*d1)] 
            sset.add(ij)
            pos_lis.append(created_pos[ij])
            col_li=colors[j]

        levels[j]=(sset,pos_lis,col_li)

    xylevels={}

    for i in range(k):
        xlevel2=[ij[0] for ij in levels[i][1]]
        ylevel2=[ij[1] for ij in levels[i][1]]
        alevel2 = [min(xlevel2)-d1/2.-0.7,max(ylevel2)+d1/2.]
        blevel2 = [max(xlevel2)+d1/2.-0.7,max(ylevel2)+d1/2.]
        clevel2 = [max(xlevel2)+d1/2.,min(ylevel2)-d1/2.]
        dlevel2 = [min(xlevel2)-d1/2.,min(ylevel2)-d1/2.]
        xylevels[i]=[alevel2,blevel2,clevel2,dlevel2]

    fig=plt.figure()#figsize=(20,20))
    ax=fig.add_subplot(111)
    for i in range(k):
        ax.add_patch(Polygon(xylevels[i],color=levels[i][2],alpha=0.1))
        xa=[j[0] for j in xylevels[i]]
        xa.append(xylevels[i][0][0])
        ya=[j[1] for j in xylevels[i]]
        ya.append(xylevels[i][0][1])
        plt.plot(xa,ya,'-',color=levels[i][2])
        nx.draw(list_of_Graphs_final[i],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.2)

    nx.draw_networkx_edges(G,created_pos,edgelist=edgelist,edge_color='k',alpha=0.2)

    plt.show()

    return created_pos

# ,d1=1.5,d2=6,d3=0,d4=.8,d5=3,d6=1,d7=0,d8=1
def plot_graph_k_n(k,n,G,list_of_Graphs_final, Gagr,d1=0,d2=2,d3=0,d4=.3,d5=1,d6=.4,d7=.2,d8=1,d9=0.3,colors_grey='gray',nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):  
    '''
    Plotting the synthetic graph after increasing the distance among layers by a parameter d1
    and dilating each layer by a parameter d1 
    '''
    # print k,n,G.nodes(),Gagr.nodes()
    if layout:
        pos=nx.spring_layout(Gagr)
    else:
        pos=nx.random_layout(Gagr)

    minPos=min(pos.keys())
    top_set=set()
    bottom_set=set()
    middle_set=set()
    levels=dict()
    created_pos={}
    if colors_grey=='gray':
        colors=['gray' for i in range (2*n)]
    elif colors_grey=='bipartite':
        colors=[]
        bipsets=bipartite.sets(G)
        for i in G.nodes():
            if i in bipsets[0]:
                colors.append('m')
            else:
                colors.append('g')
    else:
        colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    for j in range(k):

        sset=set()
        pos_lis=[]
        for i in range(n):
            ij=i+j*n
            npos=pos[i]
            created_pos[ij]=[d2*npos[0],d8*(npos[1]+j*n*d6)] 
            sset.add(ij)
            pos_lis.append(created_pos[ij])
            col_li=colors[j]

        levels[j]=(sset,pos_lis,col_li)

    xylevels={}

    for i in range(k):
        xlevel2=[ij[0] for ij in levels[i][1]]
        ylevel2=[ij[1] for ij in levels[i][1]]
        alevel2 = [min(xlevel2)-d1,max(ylevel2)+d7/2.-d3+d5]
        blevel2 = [max(xlevel2)+d9,max(ylevel2)+d7/2.+d3+d5]
        clevel2 = [max(xlevel2)+d9-d4,min(ylevel2)-d7/2.+d3-d5]
        dlevel2 = [min(xlevel2)-d1-d4,min(ylevel2)-d7/2.-d3-d5]
        xylevels[i]=[alevel2,blevel2,clevel2,dlevel2]


    fig=plt.figure(figsize=(10,10))
    ax=fig.add_subplot(111)
    for i in range(k):
        ax.add_patch(Polygon(xylevels[i],color=levels[i][2],alpha=0.1))
        xa=[j[0] for j in xylevels[i]]
        xa.append(xylevels[i][0][0])
        ya=[j[1] for j in xylevels[i]]
        ya.append(xylevels[i][0][1])
        plt.plot(xa,ya,'-',color=levels[i][2])

        nx.draw(list_of_Graphs_final[i],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.2)
    # print edgelist
    # print G.nodes()
    nx.draw_networkx_edges(G,created_pos,edgelist=edgelist,edge_color='k',alpha=0.2)

    plt.show()

    return created_pos
def plot_graph_k_nm_old(k,n,G,list_of_Graphs_final, Gagr,d1=0,d2=2,d3=0,d4=.3,d5=1,d6=.4,d7=.2,d8=1,d9=0.3,colors_grey='gray',nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):  
    '''
    Plotting the synthetic graph after increasing the distance among layers by a parameter d1
    and dilating each layer by a parameter d1 
    '''
    # print k,n,G.nodes(),Gagr.nodes()
    if layout:
        pos=nx.spring_layout(Gagr)
    else:
        pos=nx.random_layout(Gagr)

    minPos=min(pos.keys())
    top_set=set()
    bottom_set=set()
    middle_set=set()
    levels=dict()
    created_pos={}
    if colors_grey=='gray':
        colors=['gray' for i in range (2*n)]

    elif colors_grey=='bipartite':
        colors=[]
        bipsets=bipartite.sets(G)
        for i in G.nodes():
            if i in bipsets[0]:
                colors.append('m')
            else:
                colors.append('g')
    else:
        colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    bipsets=bipartite.sets(Gagr)
    print bipsets
    # print aaa
    for j in range(k):
        bipsetsin=bipartite.sets(list_of_Graphs_final[j])
        print bipsetsin

        sset=set()
        pos_lis=[]
        # for i in range(n):
        # print list_of_Graphs_final[j].nodes()
        col_li=[]
        # for i,v in enumerate(list_of_Graphs_final[j].nodes()):
        # for i in range(n):
        bipsetsin0=sorted(bipsetsin[0])
        for i,v  in enumerate(bipsetsin0):
        # for i in range(nm):
            # ij=i+j*(n+m)
            # print i,v,j,ij

            npos=pos[i]


            created_pos[v]=[d2*npos[0],d8*(npos[1]+j*n*d6)] 
            sset.add(v)
            pos_lis.append(created_pos[v])
            col_li.append('m')
            # col_li=colors[j]
            # if v in bipsets[0]:
            #     col_li.append('m')
            # else:
            #     col_li.append('g')]
        bipsetsin1=sorted(bipsetsin[1])
        for i,v  in enumerate(bipsetsin1):
        # for i in range(nm):
            # ij=i+j*(n+m)
            # print i,v,j,ij

            npos=pos[i]


            created_pos[v]=[d2*npos[0],d8*(npos[1]+j*n*d6)] 
            sset.add(v)
            pos_lis.append(created_pos[v])
            col_li.append('g')

        levels[j]=(sset,pos_lis,col_li)
        # print levels[j]
        # print created_pos
    print aaa
    xylevels={}

        # sset=set()
        # pos_lis=[]
        # for i in range(n):
        #     ij=i+j*n
        #     npos=pos[i]
        #     created_pos[ij]=[d2*npos[0],d8*(npos[1]+j*n*d6)] 
        #     sset.add(ij)
        #     pos_lis.append(created_pos[ij])
        #     col_li=colors[j]

        # levels[j]=(sset,pos_lis,col_li)

    xylevels={}

    for i in range(k):
        xlevel2=[ij[0] for ij in levels[i][1]]
        ylevel2=[ij[1] for ij in levels[i][1]]
        alevel2 = [min(xlevel2)-d1,max(ylevel2)+d7/2.-d3+d5]
        blevel2 = [max(xlevel2)+d9,max(ylevel2)+d7/2.+d3+d5]
        clevel2 = [max(xlevel2)+d9-d4,min(ylevel2)-d7/2.+d3-d5]
        dlevel2 = [min(xlevel2)-d1-d4,min(ylevel2)-d7/2.-d3-d5]
        xylevels[i]=[alevel2,blevel2,clevel2,dlevel2]


    fig=plt.figure(figsize=(10,10))
    ax=fig.add_subplot(111)
    for i in range(k):
        ax.add_patch(Polygon(xylevels[i],color='gray',alpha=0.1))
        xa=[j[0] for j in xylevels[i]]
        xa.append(xylevels[i][0][0])
        ya=[j[1] for j in xylevels[i]]
        ya.append(xylevels[i][0][1])
        plt.plot(xa,ya,'-',color='gray')
        nx.draw_networkx_nodes(list_of_Graphs_final[i],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.2)
        nx.draw_networkx_edges(list_of_Graphs_final[i],created_pos,alpha=0.2)
        # nx.draw(list_of_Graphs_final[i],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.2)
    # print edgelist
    # print G.nodes()
    # print created_pos

    nx.draw_networkx_edges(G,created_pos,edgelist=edgelist,edge_color='k',alpha=0.2)
    # for i in range(k):
    #     ax.add_patch(Polygon(xylevels[i],color=levels[i][2],alpha=0.1))
    #     xa=[j[0] for j in xylevels[i]]
    #     xa.append(xylevels[i][0][0])
    #     ya=[j[1] for j in xylevels[i]]
    #     ya.append(xylevels[i][0][1])
    #     plt.plot(xa,ya,'-',color=levels[i][2])

    #     nx.draw(list_of_Graphs_final[i],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.2)
    # # print edgelist
    # # print G.nodes()
    # nx.draw_networkx_edges(G,created_pos,edgelist=edgelist,edge_color='k',alpha=0.2)

    plt.show()

    return created_pos

def plot_graph_k_n_m(k,n,m,G,list_of_Graphs_final, Gagr,d1=0,d2=2,d3=0,d4=.3,d5=1,d6=.4,d7=.2,d8=1,d9=0.3,colors_grey='gray',nodesize=1000,withlabels=True,edgelist=[],layout=True,b_alpha=0.5):  
    '''
    Plotting the synthetic graph after increasing the distance among layers by a parameter d1
    and dilating each layer by a parameter d1 
    '''
    if layout:
        pos=nx.spring_layout(Gagr)
    else:
        pos=nx.random_layout(Gagr)
    # print pos
    # print G.nodes()
    # print edgelist
    # print list_of_Graphs_final[1].nodes()
    minPos=min(pos.keys())
    top_set=set()
    bottom_set=set()
    middle_set=set()
    levels=dict()
    created_pos={}
    if colors_grey=='gray':
        colors=['gray' for i in range (2*n)]
    elif colors_grey=='bipartite':
        colors=[]
        bipsets=bipartite.sets(G)
        for i in G.nodes():
            if i in bipsets[0]:
                colors.append('m')
            else:
                colors.append('g')
    else:
        colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    # for j in range(k):

    #     sset=set()
    #     pos_lis=[]
    #     col_li=[]
    #     for i in range(n):
    #         ij=i+j*n
    #         npos=pos[i]
    #         created_pos[ij]=[d2*npos[0],d8*(npos[1]+j*n*d6)] 
    #         sset.add(ij)
    #         pos_lis.append(created_pos[ij])
    #         col_li.append('m')
    #     for i in range(n,n+m):
    #         ij=i+j*n
    #         npos=pos[i]
    #         created_pos[ij]=[d2*npos[0],d8*(npos[1]+j*n*d6)] 
    #         sset.add(ij)
    #         pos_lis.append(created_pos[ij])
    #         col_li.append('g')
    #     levels[j]=(sset,pos_lis,col_li)
    for j in range(k):
        # bipsets=bipartite.sets(list_of_Graphs_final[j])

        sset=set()
        pos_lis=[]
        # for i in range(n):
        # print list_of_Graphs_final[j].nodes()
        col_li=[]
        for i,v in enumerate(list_of_Graphs_final[j].nodes()):
            ij=i+j*(n+m)
            # print i,v,j,ij

            npos=pos[i]
            created_pos[v]=[d2*npos[0],d8*(npos[1]+j*n*d6)] 
            sset.add(v)
            pos_lis.append(created_pos[v])
            # col_li=colors[j]
            if v in bipsets[0]:
                col_li.append('m')
            else:
                col_li.append('g')

        levels[j]=(sset,pos_lis,col_li)
        # print levels[j]
        # print created_pos
    xylevels={}

    for i in range(k):
        xlevel2=[ij[0] for ij in levels[i][1]]
        ylevel2=[ij[1] for ij in levels[i][1]]
        alevel2 = [min(xlevel2)-d1,max(ylevel2)+d7/2.-d3+d5]
        blevel2 = [max(xlevel2)+d9,max(ylevel2)+d7/2.+d3+d5]
        clevel2 = [max(xlevel2)+d9-d4,min(ylevel2)-d7/2.+d3-d5]
        dlevel2 = [min(xlevel2)-d1-d4,min(ylevel2)-d7/2.-d3-d5]
        xylevels[i]=[alevel2,blevel2,clevel2,dlevel2]


    fig=plt.figure(figsize=(10,10))
    ax=fig.add_subplot(111)
    for i in range(k):
        ax.add_patch(Polygon(xylevels[i],color='gray',alpha=0.1))
        xa=[j[0] for j in xylevels[i]]
        xa.append(xylevels[i][0][0])
        ya=[j[1] for j in xylevels[i]]
        ya.append(xylevels[i][0][1])
        plt.plot(xa,ya,'-',color='gray')
        nx.draw_networkx_nodes(list_of_Graphs_final[i],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.2)
        nx.draw_networkx_edges(list_of_Graphs_final[i],created_pos,alpha=0.2)
        # nx.draw(list_of_Graphs_final[i],created_pos,with_labels=withlabels,nodelist=list(levels[i][0]),node_color=levels[i][2],node_size=nodesize,edge_color=levels[i][2],alpha=0.2)
    # print edgelist
    # print G.nodes()
    # print created_pos
    nx.draw_networkx_edges(G,created_pos,edgelist=edgelist,edge_color='k',alpha=0.2)
    plt.axis("off")
    plt.show()

    return created_pos

def make_dict_of_edge_times(k,nmap,mapping,list_of_Graphs_final):
    nds=sorted(set(nmap.values()))
    dict_of_edges={}
    dict_of_edges_time=Counter()
    for ii in it.combinations(nds,2):
        nd=ii[0]
        dn=ii[1]
        for i in range(k):
            if list_of_Graphs_final[i].has_edge(mapping[i][nd],mapping[i][dn]):
                dict_of_edges_time[(i,i+1)]+=1
                if ii not in  dict_of_edges:
                    dict_of_edges[ii]=[(i,i+1)]
                else:
                    ko=dict_of_edges[ii].pop()
                    if isinstance(ko,tuple):
                        if ko[1]==i:
                            nka=(ko[0],i+1)
                            dict_of_edges[ii].append(nka)
                        else:
                            dict_of_edges[ii].append(ko)
                            dict_of_edges[ii].append((i,i+1))

    return dict_of_edges,dict_of_edges_time

def make_dict_of_edge_timesB(k,nmap,mapping,list_of_Graphs_final):
    nds=sorted(set(nmap.values()))
    dict_of_edges={}
    dict_of_edges_time=Counter()
    for ii in it.combinations(nds,2):
        nd=int(ii[0][1:])
        dn=int(ii[1][1:])
        for i in range(k):
            if list_of_Graphs_final[i].has_edge(mapping[i][nd],mapping[i][dn]):
                dict_of_edges_time[(i,i+1)]+=1
                if ii not in  dict_of_edges:
                    dict_of_edges[ii]=[(i,i+1)]
                else:
                    ko=dict_of_edges[ii].pop()
                    if isinstance(ko,tuple):
                        if ko[1]==i:
                            nka=(ko[0],i+1)
                            dict_of_edges[ii].append(nka)
                        else:
                            dict_of_edges[ii].append(ko)
                            dict_of_edges[ii].append((i,i+1))
               
    return dict_of_edges,dict_of_edges_time
def create_3comms_bipartite(n,m,p,No_isolates=True):
    
    import community as comm

    from networkx.algorithms import bipartite as bip
    u=0
    while  True:
        G=nx.bipartite_random_graph(n,m,p)
        list_of_isolates=nx.isolates(G)
        if No_isolates:
            G.remove_nodes_from(nx.isolates(G))
        partition=comm.best_partition(G)
        sel=max(partition.values())
        if sel==2 and nx.is_connected(G):
            break
        u+=1
        print u,sel
    ndlss=bip.sets(G)
    ndls=[list(i) for i in ndlss]
    slayer1=ndls[0]
    slayer2=ndls[1]
    layer1=[i for i,v in partition.items() if v==0]
    layer2=[i for i,v in partition.items() if v==1]
    layer3=[i for i,v in partition.items() if v==2]
    edgeList=[]
    for e in G.edges():
        if (e[0] in slayer1 and e[1] in slayer2) or (e[0] in slayer2 and e[1] in slayer1):
            edgeList.append(e)
    return G,layer1,layer2,layer3,slayer1,slayer2,edgeList,partition
def create_node_3attri_graph(G,layer1,layer2,layer3,slayer1,slayer2):
    '''G is a 3-layer graph 
    '''
   
    # layerattri1 = random.sample(G.nodes(),int(len(G.nodes())*attri1))
    # layerattri2 = random.sample(set(G.nodes())-set(layerattri1),int(len(G.nodes())*attri2))
    # layerattri3 = list(set(G.nodes())-set(layerattri1)-set(layerattri2))
    # npartition=[layerattri1,layerattri2,layerattri3]
    npartition=[slayer1,slayer2]

    layers={'layer1':layer1,'layer2':layer2,'layer3':layer3}
   
    broken_partition={}
    
    for i,v in enumerate(npartition):
        vs=set(v)
        for ii,vv in layers.items():
            papa=vs.intersection(set(vv))
            if len(papa)==len(v):
                broken_partition['a_%i_%s_s' %(i,ii)]=v
            elif len(papa)>0:
                broken_partition['b_%i_%s' %(i,ii)]=list(papa)
                vs=vs-set(vv)
            
    broken_graph=nx.Graph()
    rbroken_partition=dict()
    
    colors=[name for name,hex in matplotlib.colors.cnames.iteritems()]
    colors=list(set(colors)-set(['red','blue','green']))
   
    cl=dict()
    for i,v in broken_partition.items():
        name=i.split('_')
        for ii in v:
            rbroken_partition[ii]=i
        if name[-1]=='s':
            cl[name[1]]=colors.pop()
        elif name[0]=='b' and not cl.has_key(name[1]):
            cl[name[1]]=colors.pop()
    
    for i,v in rbroken_partition.items():

        name=v.split('_')
        broken_graph.add_node(v,color=cl[name[1]])
        edg=G[i]
        for j in edg:
            if j not in broken_partition[v]:
                if not broken_graph.has_edge(v,rbroken_partition[j]):
                    broken_graph.add_edge(v,rbroken_partition[j])
    
    return broken_graph,broken_partition,npartition
def plot_graph_bip_3comms_2set(G,broken_graph,broken_partition,npartition,layer1,layer2,layer3,d1=1.5,d2=5.,d3=0,d4=.8,nodesize=1000,withlabels=True,edgelist=[],layout=True,alpha=0.5):
    
    if layout:
        pos=nx.spring_layout(G)
    else:
        pos=nx.random_layout(G)

    top_set=set()
    bottom_set=set()
    middle_set=set()
    down=[]
    right=[]
    left=[]

    mlayer_part={}
    for i in broken_partition:
        ii=i.split('_')
        if ii[1] not in mlayer_part:
            mlayer_part[ii[1]]=set([ii[2]])
        else:
            mlayer_part[ii[1]].add(ii[2])

    layers_m=Counter()
    for k,v in mlayer_part.items():
        if len(v)==1:
            layers_m[1]+=1
        elif len(v)==2:
            layers_m[2]+=1
        elif len(v)==3:
            layers_m[3]+=1
        else:
            print k,v

    broken_pos={}
    singles=0

    for i,v in broken_partition.items():   
        name=i.split('_')
        if name[-1]=='s':
            singles+=1
        ndnd=random.choice(v)
        npos=pos[ndnd]
        if ndnd in layer1:
            broken_pos[i]=[d2*(npos[0]-d1),d2*(npos[1]+d1)] 
            top_set.add(i)
            left.append(broken_pos[i])
        elif ndnd in layer2:
            broken_pos[i]=[d2*(npos[0]+d1),d2*(npos[1]+d1)] 
            bottom_set.add(i)
            right.append(broken_pos[i])
        else:
            broken_pos[i]=[d2*npos[0],d2*(npos[1]-d1)] 
            middle_set.add(i)
            down.append(broken_pos[i])
        
    xleft=[i[0] for i in left]
    yleft=[i[1] for i in left]

    aleft = [min(xleft)-d1/2.,max(yleft)+d1/2.+d3]
    bleft = [max(xleft)+d1/2.,max(yleft)+d1/2.+3*d3]
    cleft = [max(xleft)+d1/2.,min(yleft)-d1/2.-3*d3]
    dleft = [min(xleft)-d1/2.,min(yleft)-d1/2.-d3]

    xright=[i[0] for i in right]
    yright=[i[1] for i in right]

    aright = [min(xright)-d1/2.,max(yright)+d1/2.+d3]
    bright = [max(xright)+d1/2.,max(yright)+d1/2.+3*d3]
    cright = [max(xright)+d1/2.,min(yright)-d1/2.-3*d3]
    dright = [min(xright)-d1/2.,min(yright)-d1/2.-d3]

    xdown=[i[0] for i in down]
    ydown=[i[1] for i in down]

    adown = [min(xdown)-d1/2.,max(ydown)+d1/2.+d3]
    bdown = [max(xdown)+d1/2.,max(ydown)+d1/2.+3*d3]
    cdown = [max(xdown)+d1/2.,min(ydown)-d1/2.-3*d3]
    ddown = [min(xdown)-d1/2.,min(ydown)-d1/2.-d3]

    fig=plt.figure(figsize=(20,20))
    ax=fig.add_subplot(111)

    ax.add_patch(Polygon([aleft,bleft,cleft,dleft],color='r',alpha=0.1)) 
    plt.plot([aleft[0],bleft[0],cleft[0],dleft[0],aleft[0]],[aleft[1],bleft[1],cleft[1],dleft[1],aleft[1]],'-r')

    ax.add_patch(Polygon([aright,bright,cright,dright],color='b',alpha=0.1)) 
    plt.plot([aright[0],bright[0],cright[0],dright[0],aright[0]],[aright[1],bright[1],cright[1],dright[1],aright[1]],'-b')

    ax.add_patch(Polygon([adown,bdown,cdown,ddown],color='g',alpha=0.1)) 
    plt.plot([adown[0],bdown[0],cdown[0],ddown[0],adown[0]],[adown[1],bdown[1],cdown[1],ddown[1],adown[1]],'-g')

    nodeSize=[nodesize*len(broken_partition[i]) for i in list(top_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(top_set) ]
    
    nx.draw_networkx_nodes(broken_graph,broken_pos, nodelist=list(top_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(middle_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(middle_set) ]
    
    nx.draw_networkx_nodes(broken_graph,broken_pos, nodelist=list(middle_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    nodeSize=[nodesize*len(broken_partition[i]) for i in list(bottom_set)]
    nodeColor=[broken_graph.node[i]['color'] for i in list(bottom_set) ]

    nx.draw_networkx_nodes(broken_graph,broken_pos,nodelist=list(bottom_set),node_shape='s',node_color=nodeColor,alpha=1,node_size=nodeSize)
    
    if withlabels:
        nx.draw_networkx_labels(G,pos)
    
    lay1_edges=[ed for ed in G.edges() if ed[0] in layer1 and ed[1] in layer1]
    lay2_edges=[ed for ed in G.edges() if ed[0] in layer2 and ed[1] in layer2]
    lay3_edges=[ed for ed in G.edges() if ed[0] in layer3 and ed[1] in layer3]
    
    nx.draw_networkx_edges(broken_graph,broken_pos,alpha=0.3) #0.15
    rr=nx.attribute_assortativity_coefficient(broken_graph,'color')
    title_s='%i Three vertex attributes (%i 3-layered, %i 2-layered, %i 1-layered)\n Attribute assortativity coefficient wrt layer partition = %f' %(len(npartition),layers_m[3],layers_m[2],layers_m[1],rr)  

    # title_s='%i Three vertex attributes (%i 3-layered, %i 2-layered, %i 1-layered)' %(len(npartition),layers_m[3],layers_m[2],layers_m[1])
    plt.title(title_s,{'size': '20'})
    plt.axis('off')
    plt.show()
# p1=p2=p3=0.1

# n=500
# G,J,FF,DD,JFD,edgeList = synthetic_three_level(n,p1,p2,p3,J_isolates=False,F_isolates= False, D_isolates= False)
# # print JFD.nodes()
# # print JFD.edges()
# # print F.nodes()
# # print F.edges()
# # print G.nodes()
# # print edgeList
# # print aaaa
# # print nx.isolates(G)
# # plot_graph(n,G,J,FF,DD,F,d1=2.,d2=3.,nodesize=100,withlabels=False,edgelist=edgeList,layout=True,b_alpha=0.5)
# plot_graph(n,G,J,FF,DD,JFD,d1=2.,d2=3.,nodesize=50,withlabels=False,edgelist=edgeList,layout=False,b_alpha=0.15)
# k=5
# n=10
# pp=[0.1,.1,.1,.1,.4]
# G, list_of_Graphs_final, Gagr, edgeList,nmap,mapping =synthetic_multi_level(k,n,p=pp,No_isolates=True)
# dic_of_edges=make_dict_of_edge_times(nmap,mapping,list_of_Graphs_final)

# print mapping
# print Gagr.edges()
# for i in list_of_Graphs_final:
#     print i,i.edges()
# for i in dic_of_edges:
#     print i,dic_of_edges[i]
# plot_graph_k(k,n,G, list_of_Graphs_final, Gagr, edgelist=edgeList)

# k=5
# pp=[0.21,.31,.21,.31,.4]
# # pp=[8,7,6,8,9]
# n=4
# m=6
# k=10
# n=4
# m=6
# pp=[0.19,.11,.11,.11,.14,.18,.12,.15,.13,.12]

# # pp=0.19
# G, list_of_Graphs_final, Gagr, edgeList,nmap,mapping =synthetic_multi_bipartite(k,n,m,p=pp)
# # plot_graph_k_n_m(k,n,m,G,list_of_Graphs_final, Gagr,colors_grey='bipartite', nodesize=50,withlabels=True,edgelist=edgeList,layout=True,b_alpha=0.5)
# plot_graph_k_nm(k,n+m,G,list_of_Graphs_final, Gagr,colors_grey='bipartite', nodesize=50,withlabels=False,edgelist=edgeList,layout=True,b_alpha=0.5)
# dic_of_edges,dict_of_edges_time=s3l.make_dict_of_edge_timesB(k,nmap,mapping,list_of_Graphs_final)

# k=10
# n=7
# m=6
# pp=[0.19,.11,.11,.11,.14,.18,.12,.15,.13,.12]
# G,ndls,timetoadd=create_synthetic3lgB(k,n,m,pp) 
# main_work(G,ndls,timetoadd)

# G,layer1,layer2,edgeList,partition=create_3comms_bipartite(n,m,p)
# broken_graph,broken_partition,npartition = create_node_3attri_graph(G,layer1,layer2,layer3,slayer1,slayer2)
# plot_graph(G,broken_graph,broken_partition,npartition,layer1,layer2,layer3,d1=1.4,d2=5.,d3=0.8,withlabels=False,nodesize=100,layout=False)
# print G,layer1,layer2
# print partition
# print G.edges()
# print G.nodes()