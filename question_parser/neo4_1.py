import codecs
import json

data_path="D:\pycharmProject\\rultextract\guangzhou\sqlreding\data\medical.json"

with codecs.open(data_path,'r','utf-8') as a_obj:
    datas=a_obj.readlines()
    print(type(datas))
    #共7类节点
    drugs=[]
    foods=[]#食物
    checks=[]
    departments=[]
    producers=[]
    diseases=[]#疾病
    symptoms=[]#症状
    disease_infos=[]#疾病信息

    #构建节点实体
    rels_department=[]
    rels_noteat=[]
    rels_doeat=[]
    rels_recommandeat=[]
    rels_commondrug=[]
    rels_recommanddrug=[]#疾病-热门药品关系
    rels_check=[]
    rels_drug_producer=[]#厂商药物关系

    rels_symptom=[]#疾病症状关系
    rels_acompany=[]#疾病并发关系
    rels_category=[]#疾病与科室之间的关系

    count=0
    for data in datas:
        if count==100:
            break

        data1=eval(data)

        disease_dict={}
        count+=1
        disease=data1['name']
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
        if 'symptom' in data1:
            symptoms+=data1['symptom']
            for symptom in data1['symptom']:
                rels_symptom.append([disease,symptom])
        if 'acompany' in data1:
            for acompany in data1['acompany']:
                rels_acompany.append([disease,acompany])

        if 'desc' in data1:
            disease_dict['desc']=data1['desc']
        if 'prevent' in data1:
            disease_dict['prevent']=data1['prevent']

        if 'cause' in data1:
            disease_dict['cause']=data1['cause']
        if 'get_prob' in data1:
            disease_dict['get_prob']=data1['get_prob']
        if 'easy_get' in data1:
            disease_dict['easy_get']=data1['easy_get']

        if 'cure_department' in data1:
            cure_department=data1['cure_department']
            if len(cure_department)==1:
                rels_category.append([disease,cure_department[0]])
            if len(cure_department)==2:
                big=cure_department[0]
                small=cure_department[1]
                rels_department.append([small,big])
                rels_category.append([disease,small])

            disease_dict['cure_department']=cure_department
            departments+=cure_department

        if 'cure_way' in data1:
            disease_dict['cure_way']=data1['cure_way']
        if 'cure_lasttime' in data1:
            disease_dict['cure_lasttime']=data1['cure_lasttime']
        if 'cured_prob' in data1:
            disease_dict['cured_prob']=data1['cured_prob']

        if 'common_drug' in data1:
            common_drug=data1['common_drug']
            for drug in common_drug:
                rels_commondrug.append([disease,drug])
            drugs+=common_drug

        disease_infos.append(disease_dict)

    print(len(disease_infos))
    print(rels_category)
    print(rels_symptom)
    print(rels_acompany)
    # rels_symptom, rels_acompany, rels_department, rels_category, rels_commondrug
    print(rels_department)
    print(rels_commondrug)




