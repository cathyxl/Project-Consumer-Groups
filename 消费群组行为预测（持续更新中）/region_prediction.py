from apriori import apriori

def mine_and_predict_region(list__data_set,int__minsup,int__minconf,list__region_seq,int__max_forward_num):
    stop_flag = False

    def predict_region(list__region_seq,int__max_forward_num,Tree__rules):
        def get_rules(tuple__sub_seq):
            Node__current_node=Tree__rules.root
            list__result=[]
            for int__region in tuple__sub_seq:
                if not Node__current_node.has_subnode(int__region):
                    stop_flag=True
                    return list__result
                Node__current_node=Node__current_node.get_subnode(int__region)
            else:
                if Node__current_node.rule_consequence_node is not None:
                    int__num=0
                    if Node__current_node.rule_consequence_node.int__max_consequence_len>=int__max_forward_num:
                        int__num=int__max_forward_num
                    else:
                        int__num=Node__current_node.rule_consequence_node.int__max_consequence_len
                    for tuple__consequence in Node__current_node.rule_consequence_node.storeroom.keys():
                        if len(tuple__consequence)==int__num:
                            list__result.append((tuple__consequence,Node__current_node.rule_consequence_node.storeroom[tuple__consequence]))
                        else:
                            continue
                return list__result

        list__rules=[]

        for int__i in range(2,len(list__region_seq)+2):
            if stop_flag is True:
                break
            tuple__sub_seq=tuple(list__region_seq[-1:-int__i:-1])
            list__rules.extend(get_rules(tuple__sub_seq))

        list__rules.sort(key=lambda x: -x[1])
        return list__rules[0] if len(list__rules)!=0 else None


    return predict_region(list__region_seq,int__max_forward_num,apriori(list__data_set,int__minsup,int__minconf))