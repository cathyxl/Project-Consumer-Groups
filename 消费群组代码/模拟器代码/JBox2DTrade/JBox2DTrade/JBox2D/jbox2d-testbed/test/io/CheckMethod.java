package io;

/**
 * 判断两次聚集点的时间隔怎么算
 * 
 * @author lenovo
 * 
 */
public class CheckMethod {
	/**
	 * 检测由第一个开始到第二个开始
	 */
	public static final int STARTTOSTART = 0;
	/**
	 * 检测由第一个开始到第二个结束
	 */
	public static final int STARTTOEND = 1;
	/**
	 * 检测由第一个结束到第二个开始
	 */
	public static final int ENDTOSTART = 2;
	/**
	 * 检测由第一个结束到第二个结束
	 */
	public static final int ENDTOEND = 3;
	/**
	 * 检测第一个结束在第二个结束之前,由第一个开始在第二个开始之前
	 */
	public static final int STARTTOSTART_ENDTOEND = 4;
}
