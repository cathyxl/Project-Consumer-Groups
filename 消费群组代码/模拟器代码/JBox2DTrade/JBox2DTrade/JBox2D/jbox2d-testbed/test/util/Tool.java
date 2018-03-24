package util;

public class Tool {
	/**
	 * 概率事件
	 * 
	 * @param attract_possible
	 * @return
	 */
	public static boolean probility(double attract_possible) {
		float f = (float) Math.random();
		if (f < attract_possible)
			return true;
		else
			return false;
	}
}
