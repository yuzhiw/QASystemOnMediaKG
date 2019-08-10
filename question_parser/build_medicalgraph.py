#coding=UTF-8
import os
import json
from py2neo import Graph,Node
class GZGraph:
    def __init__(self):
        cur_ir='/'.join(os.path.abspath(__file__).split('/')[:-1])
        self.data_path=os.path.join(cur_ir,'medical.json')
        self.g = Graph(
            "http://localhost:7474",
            username="neo4j",
            password="dm2019"
        )
    def read_nodes(self):
        #共7类结点
        drugs=[]#药品
        foods=[]#食物
        checks=[]#检查
        departments=[]#科室
        producers=[]#厂家
        diseases=[]#疾病
        symptoms=[]#针状

        disease_infos=[]#疾病信息
        #构建节点实体关系
        rels_department=[] #科室-科室
        rels_noteat=[]#禁吃
        rels_doeat=[]#宜吃
        rels_recommandeat=[]
        rels_commonddrug=[]
        rels_recommanddrug=[]
        rels_check=[]
        rels_drug_producer=[]#厂商-药物关系

        rels_symptom=[]#疾病症状
        rels_acompany=[]#疾病并发关系
        rels_category=[]#疾病与科室之间的关系

        count=0
        for data in open(self.data_path,encoding='utf-8'):
            disease_dict={}
            count+=1
            data_json=json.loads(data)
            disease=data_json['name']
            disease_dict['name']=disease
            diseases.append(disease)
            disease_dict['desc']=''
            disease_dict['prevent']=''
            disease_dict['cause']=''
            disease_dict['easy_get']=''
            disease_dict['cure_department']=''
            disease_dict['cure_way']=''
            disease_dict['cure_lasttime']=''
            disease_dict['symptom']=''
            disease_dict['cured_prob']=''

            if 'symptom' in data_json:
                symptoms+=data_json['symptom']
                for symptom in data_json['symptom']:
                    rels_symptom.append([disease,symptom])

            if 'acompany' in data_json:
                for acompany in data_json['acompany']:
                    rels_acompany.append([disease,acompany])

            if 'desc' in data_json:
                disease_dict['desc']=data_json['desc']
            if 'prevent' in data_json:
                disease_dict['prevent']=data_json['prevent']

            if 'cause' in data_json:
                disease_dict['cause']=data_json['cause']
            if 'get_prob' in data_json:
                disease_dict['get_prob']=data_json['get_prob']

            if 'easy_get' in data_json:
                disease_dict['easy_get']=data_json['easy_get']

            if 'cure_department' in data_json:
                cure_department=data_json['cure_department']
                if len(cure_department) ==1:
                    rels_category.append([disease,cure_department[0]])
                if len(cure_department)==2:
                    big=cure_department[0]
                    small=cure_department[1]
                    rels_department.append([small,big])
                    rels_category.append([disease,small])

                disease_dict['cure_department']=cure_department
                departments+=cure_department

            if 'cure_way' in data_json:
                disease_dict['cure_way']=data_json['cure_way']

            if 'cure_lasttime' in data_json:
                disease_dict['cure_lasttime']=data_json['cure_lasttime']

            if 'cured_prob' in data_json:
                disease_dict['cured_prob']=data_json['cured_prob']

            if 'common_drug' in data_json:
                common_drug=data_json['common_drug']
                for drug in common_drug:
                    rels_commonddrug.append([disease,drug])
                drugs+=common_drug

            if 'recommand_drug' in data_json:
                recommand_drug=data_json['recommand_drug']
                drugs+=recommand_drug
                for drug in recommand_drug:
                    rels_recommanddrug.append([disease,drug])

            if 'not_eat' in data_json:
                not_eat=data_json['not_eat']
                for _not in not_eat:
                    rels_noteat.append([disease,_not])

                foods+=not_eat
                do_eat=data_json['do_eat']
                for _do in do_eat:
                    rels_doeat.append([disease,_do])

                foods+=do_eat
                recommand_eat=data_json['recommand_eat']
                for _recommand in recommand_eat:
                    rels_recommandeat.append(([disease,_recommand]))
                foods+=recommand_eat

            if 'check' in data_json:
                check=data_json['check']
                for _check in check:
                    rels_check.append([disease,_check])
                checks+=check
            if 'drug_detail' in data_json:
                drug_detail=data_json['drug_detail']
                producer=[i.split('(')[0] for i in drug_detail]
                rels_drug_producer+=[[i.split('(')[0],i.split('(')[-1].replace(')','')] for i in drug_detail]
                producers+=producer
            disease_infos.append(disease_dict)

        return set(drugs),set(foods),set(checks),set(departments),set(producers),set(symptoms),\
    set(diseases),disease_infos,rels_check,rels_recommandeat,rels_noteat,rels_doeat,rels_department,\
        rels_commonddrug,rels_drug_producer,rels_recommanddrug,rels_symptom,rels_acompany,rels_category

    #建立结点
    def create_node(self,label,nodes):
        count=0
        for node_name in nodes:
            node=Node(label,name=node_name)
            self.g.create(node)
            count+=1
            print(count,len(nodes))
        return

    def create_diseases_nodes(self,disease_infos):
        count=0
        for disease_dict in disease_infos:
            node=Node("Disease",name=disease_dict['name'],desc=disease_dict['desc'],
                      prevent=disease_dict['prevent'],cause=disease_dict['cause'],
                      easy_get=disease_dict['easy_get'],cure_lasttime=disease_dict['cure_lasttime'],
                      cure_department=disease_dict['cure_department'],
                      cure_way=disease_dict['cure_way'],cured_prob=disease_dict['cured_prob'])
            self.g.create(node)
            count+=1
            print(count)
        return
    '''创建知识图谱实体节点类项schema'''
    def create_graphnodes(self):
        drugs, foods, checks, departments, producers, symptoms, \
        diseases, disease_infos, rels_check, rels_recommandeat, rels_noteat, rels_doeat, rels_department,\
        rels_commonddrug, rels_drug_producer, rels_recommanddrug, rels_symptom, rels_acompany, rels_category=self.read_nodes()
        self.create_diseases_nodes(disease_infos)
        self.create_node('Drug',drugs)
        print(len(drugs))
        self.create_node('Food',foods)
        self.create_node('Check',checks)
        self.create_node('Department',departments)
        self.create_node('Producer',producers)
        self.create_node('Symptom',symptoms)
        return

    def create_graphrels(self):
        Drugs,Foods,Checks,Departments,Producers,Symptoms,Diseases,disease_infos,rels_check,rels_recommandeat,\
        rels_noteat,rels_doeat,rels_department,rels_commonddrug,rels_drug_producer,rels_recommanddrug,\
        rels_symptom,rels_acompany,rels_category=self.read_nodes()
        self.create_relationship('Disease','Food',rels_recommandeat,'推荐食谱','recommand_eat')
        self.create_relationship('Disease','Food',rels_noteat,'禁吃','no_eat')
        self.create_relationship('Disease','Food',rels_doeat,'宜吃','do_eat')
        self.create_relationship('Department','Department',rels_department,'属于','belongs_to')
        self.create_relationship('Disease','Drug',rels_commonddrug,'常用药品','common_drug')
        self.create_relationship('Producer','Drug',rels_drug_producer,'生产药品','drugs_of')
        self.create_relationship('Disease', 'Drug', rels_recommanddrug, '好评药品','recommand_drug')
        self.create_relationship('Disease', 'Check', rels_check, '诊断检查','need_check')
        self.create_relationship('Disease', 'Symptom', rels_symptom, '症状','has_symptom')
        self.create_relationship('Disease', 'Disease', rels_acompany, '并发症','acompany_with')
        self.create_relationship('Disease', 'Department', rels_category, '所属科室','belongs_to')
    def create_relationship(self,start_node,end_node,edges,rel_type,rel_name):
        count=0
        set_edges=[]
        for edge in edges:
            set_edges.append('###'.join(edge))
        all=len(set(set_edges))
        for edge in set(set_edges):
            edge=edge.split('###')
            p=edge[0]
            q=edge[1]
            query="match(p:%s),(q:%s) where p.name='%s' and q.name='%s'create (p)-[rel:%s{name:'%s'}]->(q)"%(
            start_node,end_node,p,q,rel_type,rel_name)
            try:
                self.g.run(query)
                count+=1
                print(rel_type,count,all)
            except Exception as e:
                print(e)
        return
    def export_data(self):
        Drugs, Foods, Checks, Departments, Producers, Symptoms, Diseases, disease_infos, rels_check, rels_recommandeat, \
        rels_noteat, rels_doeat, rels_department, rels_commonddrug, rels_drug_producer, rels_recommanddrug, \
        rels_symptom, rels_acompany, rels_category = self.read_nodes()
        with open('drug.txt','w+') as f_drug:
            f_drug.write('\n'.join(list(Drugs)))
        with open('food.txt','w+') as f_food:
            f_food.write('\n'.join(list(Foods)))
        with open('check.txt','w+') as f_check:
            f_check.write('\n'.join(list(Checks)))
        with open('department.txt','w+') as f_depart:
            f_depart.write('\n'.join(list(Departments)))

        with open('producer.txt','w+') as f_producer:
            f_producer.write('\n'.join(list(Producers)))

        with open('symptoms.txt','w+') as f_symptom:
            f_symptom.write('\n'.join(list(Symptoms)))

        with open('disease.txt','w+') as f_disease:
            f_disease.write('\n'.join(list(Diseases)))


if __name__ == '__main__':
    handler=GZGraph()
    handler.create_graphnodes()
    handler.create_graphrels()
    handler.export_data()