package io;

import java.io.BufferedReader;
import java.io.FileNotFoundException;
import java.io.FileReader;
import java.io.IOException;
import java.io.PrintWriter;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import model.AggreDensity;
import model.Aggregation;

public class FileIO {
	public static String FileName = "aggre.txt";
	public static BufferedReader br;
	public static PrintWriter pw;
	public static PrintWriter pw1;
	public static int step;
	public static int[] lastSt;
	public static int[] st;
	public static int[] ed;
	public static int checkMethod = CheckMethod.STARTTOSTART;
	public static AggreDensity[] sl;
	public static AggreDensity[] temp;

	public static void init() {
		try {
			br = new BufferedReader(new FileReader(FileName));
			step = 0;
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
	}

	/**
	 * 读取配置文件。
	 * 
	 * @return
	 */
	public static Properties readConfigure() {
		Properties p = new Properties();
		try {
			p.load(Thread.currentThread().getContextClassLoader()
					.getResourceAsStream("configure.properties"));
		} catch (IOException e) {
			e.printStackTrace();
			return null;
		}
		return p;
	}

	/**
	 * 解析一个字符串，将其串为一个AggreDensity对象，用于存储对应聚集点的密度以及使用情况
	 * 
	 * @param s
	 * @return
	 */
	public static AggreDensity getAggreDensity(String s) {
		String[] ss = s.split(",");
		AggreDensity ad = new AggreDensity(Integer.parseInt(ss[1]),
				Float.parseFloat(ss[2]), Integer.parseInt(ss[0]));
		return ad;
	}

	/**
	 * 从文件的一行记录中提取出所有的聚集点信息
	 * 
	 * @param s
	 * @return
	 */
	public static void getAggreDensityList(String s) {
		String[] x = s.split(" ");
		sl = new AggreDensity[x.length];
		for (int i = 0; i < x.length; i++) {
			AggreDensity a = getAggreDensity(x[i]);
			sl[i] = a;
		}
	}

	/**
	 * 关闭读取文件流
	 */
	public static void close() {
		try {
			br.close();
		} catch (IOException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		if (pw != null) {
			pw.flush();
			pw.close();
		}
		if (pw1 != null) {
			pw1.flush();
			pw1.close();
		}
	}

	/**
	 * 更新一下从文件得到的聚集点信息，每经过一步减少聚集点的一步持续时间，如果聚集点持续时间为0则移除
	 * 
	 * @param ag
	 */
	public static void updateList(List<AggreDensity> ag) {
		if (ag == null || ag.isEmpty()) {
			return;
		}
		for (AggreDensity a : ag) {
			a.T--;

			if (a.T == 0) {
				a.end = true;
			}
			if (a.density < Aggregation.AGGRE_CRITICAL_VALUE) {
				a.end = true;
			}
		}
	}

	/**
	 * 根据得到的一行聚集点数据决定如何更新数据
	 * 
	 * @param ag
	 *            暂时的聚集点存储列表
	 * @param la
	 *            一行聚集点数据转化的聚集点列表
	 */
	public static void updateList(List<AggreDensity> ag, int lineNum) {
		if (ag == null || ag.isEmpty()) {
			return;
		}
		for (AggreDensity a : ag) {
			a.T--;
			if (a.T == 0) {
				a.end = true;
				a.endLine = lineNum;
			}
			if (a.density < Aggregation.AGGRE_CRITICAL_VALUE) {
				a.end = true;
				a.endLine = lineNum;
			}
		}
	}

	// 数据比较
	// 异步实验数据处理
	public static int[] dataCompare(String dir, String condition)
			throws IOException {
		String fileshop = dir + "\\" + "shop_" + condition + "step.txt";
		String fileaggre = dir + "\\" + "aggre_" + condition + "step.txt";
		BufferedReader brs;
		BufferedReader bra;
		int cmp = 0, three = 0, maxpass = 0, two = 0, del = 0;// cmp同步和异步之间的比较，maxpass最长链的长度,del
																// 计数
		int pass = 1, pass1 = 1, pass2 = 0;
		List event = new ArrayList();
		List avepass = new ArrayList();// 事件平均长度
		try {
			brs = new BufferedReader(new FileReader(fileshop));
			bra = new BufferedReader(new FileReader(fileaggre));
			// 开始分析文件
			String s, a;
			int n = -1, nn = 0, max = -1, m = -1;
			while ((s = brs.readLine()) != null && (a = bra.readLine()) != null) {
				avepass.clear();
				String[] ss = s.split(" ");
				String[] aa = a.split(" ");
				for (int i = 0; i < ss.length; i++)
					avepass.add(1);
				if (nn > 1) {
					int en = 0;
					for (int i = 0; i < event.size(); i++)
						en += (Integer) event.get(i);
					en = en / event.size();
					if (ss.length < (en * 0.6)) {
						del++;
						nn++;
						continue;
					}
				}
				event.add(ss.length);
				List listoftwo = new ArrayList();
				List listofthree = new ArrayList();
				nn++;
				for (int i = 0; i < ss.length; i++) {

					if (ss.length > 1)
						if (!listoftwo.contains(Integer.parseInt(ss[i])))
							listoftwo.add(Integer.parseInt(ss[i]));
					int k = i;
					for (int j = i + 1; j < ss.length; j++) {
						n = Integer.parseInt(ss[k]) % 100;
						m = Integer.parseInt(ss[j]) / 100;
						if (n == m) {
							k = j;
							pass++;
						}

					}
					if (pass > max) {
						max = pass;
					}
					pass = 1;
				}
				maxpass += max;

				for (int i = 2; i <= max; i++) {
					int flag = 0;
					for (int k = 0; k < ss.length; k++) {
						int h = k, h1 = k;
						for (int j = k + 1; j < ss.length; j++) {
							n = Integer.parseInt(ss[h]) % 100;
							m = Integer.parseInt(ss[j]) / 100;
							if (n == m) {
								if (pass1 == 1)
									flag = j;
								h = j;
								pass1++;
							}
							if (pass1 >= i) {
								avepass.add(pass1);
								int ntwo = (Integer.parseInt(ss[h1]) / 100 + 0)
										* 100 + Integer.parseInt(ss[j]) % 100;
								int nthree = Integer.parseInt(ss[h1]) * 100
										+ Integer.parseInt(ss[j]) % 100;
								if (!listoftwo.contains(ntwo))
									listoftwo.add(ntwo);
								if (!listofthree.contains(nthree))
									listofthree.add(nthree);
								j = flag;
								h = h1;
								pass1 = 1;
							}
						}
						pass1 = 1;
					}
				}
				int avep = 0;
				for (int i = 0; i < avepass.size(); i++) {
					avep += (Integer) avepass.get(i);
				}

				pass2 += avep / avepass.size();
				for (int j = 0; j < aa.length; j++) {
					if (aa.length > 1)
						if (listoftwo.contains(Integer.parseInt(aa[j])))
							cmp++;
				}
				two += listoftwo.size();
				three += listofthree.size();
				listofthree.clear();
				listoftwo.clear();
				max = -1;
			}
			two = (two / (10 - del)) * 2;
			maxpass = maxpass / (10 - del);
			three = three / (10 - del);
			cmp = cmp / (10 - del);
			pass2 = pass2 / (10 - del);
			// System.out.println(cmp);
		} catch (FileNotFoundException e) {
			// TODO Auto-generated catch block
			e.printStackTrace();
		}
		int[] data = { cmp, three, maxpass, two, pass2 };
		return data;
	}

	// 异步统计s-s&&e-e
	public static int getTwo3(String FileName) throws IOException {
		if (!FileName.equals(" ")) {
			FileIO.FileName = FileName;
		}
		int[] sid = new int[12];
		for (int i = 0; i < 12; i++)
			sid[i] = 0;
		int sum = 0;// 计数
		int max = 0;
		int ave = 0;
		int count = 0;
		List la = new ArrayList();// 用于储存事件发生的两个shop的ID
		init();
		// 开始分析文件
		String s;
		boolean first = true;
		while ((s = br.readLine()) != null) {
			String[] a = s.split(" ");
			String[] c = s.split(" ");
			for (int i = 0; i < a.length; i++) {
				String[] b = a[i].split(",");
				a[i] = b[1];// 存储目前开始聚集或上一个发生聚集事件的商店ID
				c[i] = b[2];// 存储目前结束聚集或上一个结束聚集事件的商店ID
			}
			if (first == true) {
				st = new int[a.length];
				ed = new int[c.length];
				lastSt = new int[a.length];
				for (int i = 0; i < a.length; i++) {
					st[i] = Integer.parseInt(a[i]);
					ed[i] = Integer.parseInt(c[i]);
				}
				first = false;
			} else {
				for (int i = 0; i < a.length; i++) {
					if (st[i] != Integer.parseInt(a[i]) && ed[i] != st[i]) {
						if (st[i] == -1) {
							sid[Integer.parseInt(a[i]) - 1]++;
						} else {
							lastSt[i] = st[i];
						}
					}
					if (st[i] == Integer.parseInt(a[i]) && ed[i] == lastSt[i]
							&& st[i] != -1 && ed[i] != st[i]) {
						int nm = ed[i] * 100 + Integer.parseInt(a[i]);
						int mn = Integer.parseInt(a[i]) * 100 + ed[i];
						if (!la.contains(nm)) {
							la.add(nm);
							la.add(mn);
							pw1.print(nm + " ");
							sum = sum + 2;
						} else {
							int ns = 0;
							int na = 0;
							for (int j = 0; j < a.length; j++) {
								if (a[i] == a[j])
									na++;
								if (st[i] == Integer.parseInt(a[j]))
									na++;
								if (st[j] == st[i])
									ns++;
								if (st[j] == Integer.parseInt(a[i]))
									ns++;
							}
							if (na > ns) {
								pw1.print(nm + " ");
								sum++;
							}
						}
					}
				}
				for (int i = 0; i < a.length; i++) {
					st[i] = Integer.parseInt(a[i]);
					ed[i] = Integer.parseInt(c[i]);
				}
			}
		}
		pw1.println();
		pw1.flush();
		return sum;

	}

	// 异步统计e-s
	public static int[] getTwo2(String FileName) throws IOException {
		if (!FileName.equals(" ")) {
			FileIO.FileName = FileName;
		}
		int[] sid = new int[12];
		for (int i = 0; i < 12; i++)
			sid[i] = 0;
		int sum = 0;// 计数
		int max = 0;
		int ave = 0;
		int count = 0;
		List la = new ArrayList();// 用于储存事件发生的两个shop的ID
		init();
		// 开始分析文件
		String s;
		boolean first = true;
		while ((s = br.readLine()) != null) {
			String[] a = s.split(" ");
			String[] c = s.split(" ");
			for (int i = 0; i < a.length; i++) {
				String[] b = a[i].split(",");
				a[i] = b[1];// 存储目前开始聚集或上一个发生聚集事件的商店ID
				c[i] = b[2];// 存储目前结束聚集或上一个结束聚集事件的商店ID
			}
			if (first == true) {
				st = new int[a.length];
				ed = new int[c.length];
				for (int i = 0; i < a.length; i++) {
					st[i] = Integer.parseInt(a[i]);
					ed[i] = Integer.parseInt(c[i]);
				}
				first = false;
			} else {
				for (int i = 0; i < a.length; i++) {
					if (st[i] != Integer.parseInt(a[i]) && ed[i] == st[i]) {
						if (st[i] == -1) {
							sid[Integer.parseInt(a[i]) - 1]++;
						} else {
							int nm = ed[i] * 100 + Integer.parseInt(a[i]);
							int mn = Integer.parseInt(a[i]) * 100 + ed[i];
							if (!la.contains(nm)) {
								la.add(nm);
								la.add(mn);
								pw1.print(nm + " ");
								sum++;
							} else {
								int ns = 0;
								int na = 0;
								for (int j = 0; j < a.length; j++) {
									if (a[i] == a[j])
										na++;
									if (st[i] == Integer.parseInt(a[j]))
										na++;
									if (st[j] == st[i])
										ns++;
									if (st[j] == Integer.parseInt(a[i]))
										ns++;
								}
								if (na > ns) {
									pw1.print(nm + " ");
									sum++;
								}
							}
						}
					}
				}
				for (int i = 0; i < a.length; i++) {
					st[i] = Integer.parseInt(a[i]);
					ed[i] = Integer.parseInt(c[i]);
				}
			}
		}
		pw1.println();
		pw1.flush();
		int[] result = { sum, ave, max };
		return result;

	}

	// 异步聚集影响统计s-s及数据处理
	public static int[] getTwo1(String FileName) throws IOException {
		if (!FileName.equals(" ")) {
			FileIO.FileName = FileName;
		}
		int[] sid = new int[12];
//		for (int i = 0; i < 12; i++)
//			sid[i] = 0;
		int sum = 0;// 计数
//		int max = 0;
//		int ave = 0;
//		int count = 0;
		List<Integer> la = new ArrayList<Integer>();//暂时存储事件发生的ID，将摇摆情况预先载入
		List<Integer> nodes = new ArrayList<Integer>();// 用于储存事件发生的两个shop的ID
		init();
		// 开始分析文件
		String s;
		boolean first = true;
		while ((s = br.readLine()) != null) {
			String[] a = s.split(" ");
			for (int i = 0; i < a.length; i++) {
				String[] b = a[i].split(",");
				a[i] = b[1];// 存储商店ID
			}
			if (first == true) {
				st = new int[a.length];
				for (int i = 0; i < a.length; i++) {
					st[i] = Integer.parseInt(a[i]);
				}
				first = false;
			} else {
				for (int i = 0; i < a.length; i++) {
					if (st[i] != Integer.parseInt(a[i])) {
						if (st[i] == -1) {
							st[i] = Integer.parseInt(a[i]);
						} else {
							int nm = st[i] * 100 + Integer.parseInt(a[i]);
							int mn = Integer.parseInt(a[i]) * 100 + st[i];
							if (!la.contains(nm)&&!la.contains(mn)) {
								la.add(nm);
								la.add(mn);
								nodes.add(nm);
//								if (sid[st[i] - 1] > max - 1) {
//									max = sid[st[i] - 1] + 1;
//									sid[st[i] - 1] = 0;
//								}
//								ave = ave + sid[st[i] - 1] + 1;
//								count++;
								pw1.print(nm + " ");
//								sum++;
							} else {
								int ns = 0;
								int na = 0;
								for (int j = 0; j < a.length; j++) {
									if (a[i] == a[j])
										na++;
									if (st[i] == Integer.parseInt(a[j]))
										na++;
									if (st[j] == st[i])
										ns++;
									if (st[j] == Integer.parseInt(a[i]))
										ns++;
								}
								if (na > ns) {
									nodes.add(nm);
//									if (sid[st[i] - 1] > max - 1) {
//										max = sid[st[i] - 1] + 1;
//										sid[st[i] - 1] = 0;
//									}
//									ave = ave + sid[st[i] - 1] + 1;
//									count++;
									pw1.print(nm + " ");
//									sum++;
								}
							}
							st[i] = Integer.parseInt(a[i]);
						}
					}
				}
			}
		}
		for(int i=0;i<nodes.size();i++){
			for(int j=i;j<nodes.size();j++){
				if(nodes.get(i)%100==nodes.get(j)/100&&nodes.get(i)!=nodes.get(j)){
					sum++;
					pw1.print(nodes.get(i)/100+nodes.get(j)/100+" ");
				}
			}
		}
//		if (count > 0)
//			ave = ave / count;
		pw1.println();
		pw1.flush();
		sum=sum+nodes.size();
		int[] result = { sum };
		return result;
	}

	public static int getThree1(String FileName) throws IOException {
		if (!FileName.equals(" ")) {
			FileIO.FileName = FileName;
		}

		int sum = 0;// 计数
		List la = new ArrayList();// 用于储存事件发生的两个shop的ID
		init();
		// 开始分析文件
		String s;
		boolean first = true;
		while ((s = br.readLine()) != null) {
			String[] a = s.split(" ");
			for (int i = 0; i < a.length; i++) {
				String[] b = a[i].split(",");
				a[i] = b[1];

			}
			if (first == true) {
				st = new int[a.length];

				for (int i = 0; i < a.length; i++) {
					st[i] = Integer.parseInt(a[i]);
				}

				first = false;
			} else {
				for (int i = 0; i < a.length; i++) {
					if (st[i] == Integer.parseInt(a[i]) || st[i] == -1)
						continue;
					else {
						int nm = st[i] * 100 + Integer.parseInt(a[i]);
						int mn = Integer.parseInt(a[i]) * 100 + st[i];
						if (!la.contains(nm)) {
							la.add(nm);
							la.add(mn);
							pw1.print(nm + " ");
							sum++;
						} else {
							int ns = 0;
							int na = 0;
							for (int j = 0; j < a.length; j++) {
								if (a[i] == a[j])
									na++;
								if (st[i] == Integer.parseInt(a[j]))
									na++;
								if (st[j] == st[i])
									ns++;
								if (st[j] == Integer.parseInt(a[i]))
									ns++;
							}
							if (na > ns) {
								pw1.print(nm + " ");
								sum++;
							}
						}
					}
					// }
				}
				for (int i = 0; i < a.length; i++) {
					st[i] = Integer.parseInt(a[i]);
				}
			}
		}
		pw1.println();
		pw1.flush();
		return sum;
	}

	/**
	 * 从数量为n的数据中得到其平均值
	 * 
	 * @param FileName
	 * @param n
	 * @return
	 * @throws IOException
	 */
	public static int[] getTwoAll1(String FileName, int n) throws IOException {
		int sum = 0, max = 0, ave = 0;
		pw1 = new PrintWriter(FileName + "_" + "s-s_step" + ".txt");
		for (int i = 1; i <= n; i++) {
			String newFileName = FileName + "_" + i + ".txt";
			int[] re = FileIO.getTwo1(newFileName);
			sum += re[0];
		}
		close();
		sum = sum / n;
		int[] data = { sum, ave, max };
		return data;
	}

	public static int getTwoAll5(String FileName, int n) throws IOException {
		int sum = 0;
		pw1 = new PrintWriter(FileName + "_" + "e-e_step" + ".txt");
		for (int i = 1; i <= n; i++) {
			String newFileName = FileName + "_" + i + ".txt";
			int re = FileIO.getTwo3(newFileName);
			sum += re;
		}
		close();
		sum = sum / n;
		return sum;
	}

	// e-s异步分析
	public static int[] getTwoAll4(String FileName, int n) throws IOException {
		int sum = 0, max = 0, ave = 0;
		pw1 = new PrintWriter(FileName + "_" + "e-s_step" + ".txt");
		for (int i = 1; i <= n; i++) {
			String newFileName = FileName + "_" + i + ".txt";
			int[] re = FileIO.getTwo2(newFileName);
			sum += re[0];
			ave += re[1];
			max += re[2];
		}
		close();
		sum = sum / n;
		ave = ave / n;
		max = max / n;
		int[] data = { sum, ave, max };
		return data;
	}

	public static int getTwoAll(String FileName, int n) throws IOException {
		int sum = 0;
		pw = new PrintWriter(FileName + "_e-s_" + "step" + ".txt");
		for (int i = 1; i <= n; i++) {
			String newFileName = FileName + "_" + i + ".txt";
			sum += FileIO.getTwo(newFileName, CheckMethod.ENDTOSTART);
		}
		close();
		return sum / n;
	}

	public static int getTwoAll2(String FileName, int n) throws IOException {
		int sum = 0;
		pw = new PrintWriter(FileName + "_s-s_" + "step" + ".txt");
		for (int i = 1; i <= n; i++) {
			String newFileName = FileName + "_" + i + ".txt";
			sum += FileIO.getTwo(newFileName, CheckMethod.STARTTOSTART);

		}
		close();
		return sum / n;
	}

	public static int getTwoAll3(String FileName, int n) throws IOException {
		int sum = 0;
		pw = new PrintWriter(FileName + "_e-e_" + "step" + ".txt");
		for (int i = 1; i <= n; i++) {
			String newFileName = FileName + "_" + i + ".txt";
			sum += FileIO
					.getTwo(newFileName, CheckMethod.STARTTOSTART_ENDTOEND);

		}
		close();
		return sum / n;
	}

	public static int getThreeAll1(String FileName, int n) throws IOException {
		int sum = 0;
		pw1 = new PrintWriter(FileName + "_" + "step" + ".txt");
		for (int i = 1; i <= n; i++) {
			String newFileName = FileName + "_" + i + ".txt";
			sum += FileIO.getThree1(newFileName);
		}
		close();
		return sum / n;
	}

	// public static int getThreeAll(String FileName, int n) throws IOException
	// {
	// int sum = 0;
	// for (int i = 1; i <= n; i++) {
	// String newFileName = FileName + "_" + i + ".txt";
	// sum += FileIO.getThree(newFileName);
	// }
	// return sum / n;
	// }

	// 统计得到的连续三个相邻的聚集的信息(以默认值开始到开始为准)
	// public static int getThree(String FileName) throws IOException {
	// if (!FileName.equals(" ")) {
	// FileIO.FileName = FileName;
	// }
	// // System.out.println(FileName);
	// int sum = 0;// 计数
	// List<AggreDensity> la = new ArrayList<AggreDensity>();// 用于存储聚集点的序列
	// init();
	// // 开始分析文件
	// String s;
	// while ((s = br.readLine()) != null) {
	//
	// List<AggreDensity> get = getAggreDensityList(s);
	// for (AggreDensity a : get) {
	// if (la.contains(a)) {
	// continue;
	// } else {
	// a.setBefore(la.size());
	// for (AggreDensity ax : la) {
	// if (ax.endstep >= 0) {
	// a.addBefore(1);
	// sum += ax.getBefore();
	// }
	// }
	// la.add(a);
	// }
	// }
	// updateList(la);
	//
	// }
	// close();
	// return sum;
	// }

	/**
	 * 根据决定好的判断间隔方法来得到E2T的个数
	 * 
	 * @param FileName
	 *            储存文件
	 * @param x
	 *            间隔方法
	 * @return
	 * @throws IOException
	 *             当文件发生异常时抛出
	 */
	public static int getTwo(String FileName, int x) throws IOException {
		if (!FileName.equals(" ")) {
			FileIO.FileName = FileName;
		}
		int sum = 0;// 计数
		List<AggreDensity> la = new ArrayList<AggreDensity>();// 用于存储聚集点的序列
		init();
		// 开始分析文件
		String s;
		int lineNum = 0;
		Boolean first = true;
		while ((s = br.readLine()) != null) {
			lineNum++;
			if (x == CheckMethod.STARTTOSTART_ENDTOEND
					|| x == CheckMethod.ENDTOSTART
					|| x == CheckMethod.STARTTOSTART) {
				getAggreDensityList(s);
				if (first) {
					temp = new AggreDensity[sl.length];
					for (int i = 0; i < sl.length; i++) {
						temp[i] = sl[i];
						if (temp[i].use == 1
								&& temp[i].density >= Aggregation.AGGRE_CRITICAL_VALUE) {
							temp[i].startLine = lineNum;
							la.add(temp[i]);
						} else
							temp[i].startLine = -1;
					}
					first = false;
				} else {
					for (int i = 0; i < sl.length; i++) {
						if (sl[i].use == 1
								&& temp[i].use == 1
								&& temp[i].density >= Aggregation.AGGRE_CRITICAL_VALUE
								&& sl[i].density >= Aggregation.AGGRE_CRITICAL_VALUE) {
							continue;
						} else if ((sl[i].use != 1 || sl[i].density < Aggregation.AGGRE_CRITICAL_VALUE)
								&& temp[i].use == 1
								&& temp[i].density >= Aggregation.AGGRE_CRITICAL_VALUE) {
							for (AggreDensity a : la) {
								if (a.equals(temp[i])) {
									a.endLine = lineNum;
								}
							}
							temp[i] = sl[i];
						} else if (sl[i].use == 1
								&& temp[i].density < Aggregation.AGGRE_CRITICAL_VALUE
								&& sl[i].density >= Aggregation.AGGRE_CRITICAL_VALUE) {
							temp[i] = sl[i];
							temp[i].startLine = lineNum;
							la.add(temp[i]);
						}
					}
				}
			}
			if (x == CheckMethod.STARTTOSTART) {
				for (AggreDensity ad : la) {
					for (AggreDensity ad2 : la) {
						if (ad2.startLine - ad.startLine <= Aggregation.STEP
								&& ad2.startLine > ad.startLine) {
							if (!ad.child.contains(ad2)) {
								ad.child.add(ad2);
								int k = ad.aggreID * 100 + ad2.aggreID;
								sum++;
								pw.print(k + " ");
							}
						}
					}
				}
			} else if (x == CheckMethod.ENDTOSTART) {
				for (AggreDensity ad : la) {
					for (AggreDensity ad2 : la) {
						if (ad2.startLine > ad.endLine
								&& ad2.startLine - ad.endLine <= Aggregation.STEP
								&& ad.endLine != -1) {
							if (!ad.child.contains(ad2)) {
								ad.child.add(ad2);
								int k = ad.aggreID * 100 + ad2.aggreID;
								sum++;
								pw.print(k + " ");
							}
						}
					}
				}
			} else if (x == CheckMethod.STARTTOSTART_ENDTOEND) {
				for (AggreDensity ad : la) {
					for (AggreDensity ad2 : la) {
						if (ad2.startLine > ad.startLine
								&& ad2.startLine - ad.startLine <= Aggregation.STEP
								&& ad2.endLine - ad.endLine <= Aggregation.STEP
								&& ad2.endLine > ad.endLine && ad.endLine != -1
								&& ad.startLine != -1) {
							if (!ad.child.contains(ad2)) {
								ad.child.add(ad2);
								int k = ad.aggreID * 100 + ad2.aggreID;
								sum++;
								pw.print(k + " ");
							}
						}
					}
				}
			}
		}
		pw.println();
		pw.flush();
		return sum;
	}

	/**
	 * 根据决定好的判断间隔方法来得到E3T的个数
	 * 
	 * @param FileName
	 *            储存文件
	 * @param x
	 *            间隔方法
	 * @return
	 * @throws IOException
	 *             当文件发生异常时抛出
	 */
	public static int getThree(String FileName, int x) throws IOException {
		if (!FileName.equals(" ")) {
			FileIO.FileName = FileName;
		}
		int sum = 0;// 计数
		List<AggreDensity> la = new ArrayList<AggreDensity>();// 用于存储聚集点的序列
		init();
		// 开始分析文件
		String s;
		int lineNum = 0;
		// while ((s = br.readLine()) != null) {
		// lineNum++;
		// if (x == CheckMethod.STARTTOSTART) {
		// List<AggreDensity> get = getAggreDensityList(s);
		// for (AggreDensity a : get) {
		// if (la.contains(a)) {
		// continue;
		// } else {
		// a.setBefore(la.size());
		// for (AggreDensity ax : la) {
		// sum += ax.getBefore();
		// }
		// la.add(a);
		// }
		// }
		// updateList(la);
		// } else if (x == CheckMethod.ENDTOSTART) {
		// List<AggreDensity> get = getAggreDensityList(s);
		// for (AggreDensity a : get) {
		// if (la.contains(a)) {
		// continue;
		// } else {
		// for (AggreDensity ax : la) {
		// if (ax.getEnd()) {
		// a.addBefore(la.size());
		// sum += ax.getBefore();
		// }
		// }
		// la.add(a);
		// }
		// }
		// updateList(la, lineNum);
		// }
		// }
		close();
		return sum;
	}
}
