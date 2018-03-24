package model;

import io.FileIO;

import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

public class AggreDensity {
	public static Properties configure = FileIO.readConfigure();
	public int aggreID;
	public float density;
	public int use;
	public int startLine;
	public int endLine;
	/**
	 * 对应聚集点的持续时间，主要用于从开始到开始的情况
	 */
	public int T;
	public int endstep;
	public List<AggreDensity> child;
	/**
	 * 该属性用于存储有多少正好在该点之前的点，只用于计算连续三次的聚集点
	 */
	private int before;
	/**
	 * 该属性用于存储是否已经进入结束状态，主要用于由结束到开始的情况
	 */
	public boolean end;

	public AggreDensity(int aggreID, float density, int use) {
		super();
		this.aggreID = aggreID;
		this.density = density;
		this.use = use;
		this.endstep = Aggregation.STEP;
		this.before = 0;
		this.T = Aggregation.Default_T;
		this.startLine = -1;
		this.endLine = -1;
		this.end = false;
		this.child = new ArrayList<AggreDensity>();
	}

	@Override
	public int hashCode() {
		final int prime = 31;
		int result = 1;
		result = prime * result + aggreID;
		return result;
	}

	@Override
	public boolean equals(Object obj) {
		if (this == obj)
			return true;
		if (obj == null)
			return false;
		if (getClass() != obj.getClass())
			return false;
		AggreDensity other = (AggreDensity) obj;
		if (aggreID != other.aggreID)
			return false;
		return true;
	}

	public void setBefore(int x) {
		this.before = x;
	}

	public int getBefore() {
		return this.before;
	}

	/**
	 * 为before加上x的值
	 * 
	 * @param x
	 */
	public void addBefore(int x) {
		this.before += x;
	}

	/**
	 * 调用该方法表示对应聚集点结束聚集，不可逆
	 */
	public void setEnd() {
		this.end = true;
	}

	public boolean getEnd() {
		return this.end;
	}
}
