def apriori(data_set,min_support,min_confidence):
    def generate_all_frequent_patterns(data_set,min_support):
        def is_sub_pattern(sub, father):
            father_len=len(father)
            sub_len=len(sub)
            if sub_len>father_len:
                return False
            def check_consistency(start_position):
                i=start_position
                for item in sub:
                    if father[i]!=item:
                        return False
                    i+=1
                return True
            for i in range(0,father_len-sub_len+1):
                if father[i]==sub[0]:
                    if check_consistency(i)==True:
                        return True
            return False

        def  from_Ck_to_Lk(Ck):
            """
                    计算Ck中的项集在数据集合data_set(记录或者transactions)中的支持度,  
                    返回满足最小支持度的项集的集合。
            """
            lenCk=len(Ck)
            support_list=[0 for n in range(lenCk)]
            for transaction in data_set:
                for i in range(0,lenCk):
                    if is_sub_pattern(Ck[i],transaction)==True:
                        support_list[i]+=1
            Lk=[]
            for i in range(0, lenCk):
                support=support_list[i]
                if support>=min_support:
                    Lk.append((Ck[i],support))
            return Lk

        def create_L1():
            C1 = []
            for transaction in data_set:
                for item in transaction:
                    if [item] not in C1:
                        C1.append([item])
            C1.sort()
            return from_Ck_to_Lk(C1)

        def create_Lk(L):
            L_len = len(L)
            itemset_len = len(L[0][0])
            Ck = []
            if itemset_len==1:
                for i in range(0,L_len):
                    for j in range(0,L_len):
                        new_ele=[]
                        new_ele.append(L[i][0][0])
                        new_ele.append(L[j][0][0])
                        Ck.append(new_ele)
            else:
                for i in range(0,L_len):
                    for j in range(i+1,L_len):
                        flag=True
                        for k in range(0,itemset_len-1):
                            if L[i][0][k]!=L[j][0][k+1]:
                                flag=False
                                break
                        if flag==True:
                            new_ele=L[j][0].copy()
                            new_ele.append(L[i][0][itemset_len-1])
                            Ck.append(new_ele)
                        flag=True
                        for k in range(0,itemset_len-1):
                            if L[j][0][k]!=L[i][0][k+1]:
                                flag=False
                                break
                        if flag==True:
                            new_ele=L[i][0].copy()
                            new_ele.append(L[j][0][itemset_len-1])
                            Ck.append(new_ele)
            Ck.sort()
            Lk=from_Ck_to_Lk(Ck)
            return Lk

        def create_all_Lk():
            LS=[]
            LS.append(create_L1())
            i=0
            while True:
                Lk=create_Lk(LS[i])
                if Lk:
                    LS.append(Lk)
                    i += 1
                else:
                    break
            return LS

        return create_all_Lk()


    def discovering_rules(all_Lk_set,min_confidence):
        class RuleConsequenceNode:
            def __init__(self):
                self.storeroom={}
                self.int__max_consequence_len=0

            def add_rule_consequence(self,tuple__consequence,float__confidence):
                if len(tuple__consequence)>self.int__max_consequence_len:
                    self.int__max_consequence_len=len(tuple__consequence)
                self.storeroom[tuple__consequence]=float__confidence


        class Node:
            def __init__(self, region_id):
                self.region_id = region_id
                self.subnodes = {}
                self.rule_consequence_node=None

            def add_subnode(self, subnode):
                self.subnodes[subnode.region_id] = subnode

            def has_subnode(self,int__subnode_id):
                if int__subnode_id in self.subnodes: return True
                else: return False

            def get_subnode(self,int__subnode_id):
                return self.subnodes[int__subnode_id]

        class Tree:
            def __init__(self):
                self.root = Node(None)

            def add_association_rule(self,tuple__left_seq,tuple__right_seq,float__confidence):
                Node__current_node=self.root
                for int__region_id in tuple__left_seq[::-1]:
                    if not Node__current_node.has_subnode(int__region_id):
                        new_node=Node(int__region_id)
                        Node__current_node.add_subnode(new_node)
                        Node__current_node = new_node
                    else:
                        Node__current_node = Node__current_node.get_subnode(int__region_id)
                if Node__current_node.rule_consequence_node is None:
                    Node__current_node.rule_consequence_node = RuleConsequenceNode()
                Node__current_node.rule_consequence_node.add_rule_consequence(tuple__right_seq, float__confidence)

        rule_tree = Tree()

        def generate_rules(sequence_tuple):
            sequence=sequence_tuple[0]
            sequence_support=sequence_tuple[1]
            for i in range(1, len(sequence)):
                left_seq=sequence[0:i]
                right_seq=sequence[i:]
                for seq_tuple in all_Lk_set[i-1]:
                    if seq_tuple[0]==left_seq:
                        confidence=sequence_support/seq_tuple[1]
                        if confidence>=min_confidence:
                            rule_tree.add_association_rule(tuple(left_seq),tuple(right_seq),confidence)
                        break

        if len(all_Lk_set)==1:
            return[]
        else:
            for i in range(1,len(all_Lk_set)):
                for j in all_Lk_set[i]:
                    generate_rules(j)

        return rule_tree

    return discovering_rules(generate_all_frequent_patterns(data_set,min_support),min_confidence)
