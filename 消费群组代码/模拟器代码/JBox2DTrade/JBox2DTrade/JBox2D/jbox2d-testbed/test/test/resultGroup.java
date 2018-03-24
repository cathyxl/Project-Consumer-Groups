package test;

import java.util.ArrayList;

public class resultGroup {
	public resultGroup() {
		this.count = 0;
		this.reGroup = new ArrayList<String>();
		this.b = false;
	}

	public boolean b;// 计算该组是否被重复计算为属于hit
	public int count;// 计数器
	public ArrayList<String> reGroup;

	public ArrayList<String> getReGroup() {
		return reGroup;
	}

	public void setReGroup(ArrayList<String> reGroup) {
		this.reGroup = reGroup;
	}
}
