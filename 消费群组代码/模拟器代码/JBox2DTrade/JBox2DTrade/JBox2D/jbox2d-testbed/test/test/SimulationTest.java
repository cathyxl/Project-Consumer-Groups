package test;

import io.FileIO;

import java.awt.event.KeyEvent;
import java.io.FileNotFoundException;
import java.io.IOException;
import java.io.PrintWriter;
//import java.sql.ResultSet;
import java.util.ArrayList;
import java.util.List;
import java.util.Properties;

import model.Aggregation;
import model.Mall;
import model.Mall.Shop;
import model.People;
import model.PeopleGroup;

import org.jbox2d.common.MathUtils;
import org.jbox2d.common.Vec2;
import org.jbox2d.dynamics.Body;
import org.jbox2d.testbed.framework.TestbedSettings;
import org.jbox2d.testbed.framework.TestbedTest;

import util.Tool;

public class SimulationTest extends TestbedTest {
	/**
	 * 配置信息。
	 */
	public static Properties configure;

	public Mall mall;

	/**
	 * PeopleGroup集合。
	 */
	public List<PeopleGroup> pgList = new ArrayList<PeopleGroup>();
	/**
	 * 存储当前存在的宣传点
	 */
	public List<Body> aggre = new ArrayList<Body>();

	public List<Body> people = new ArrayList<Body>();
	/**
	 * 记录每个STEP里所有人的坐标。
	 */
	public static final String PATH = "path.txt";
	public PrintWriter pw_path;
	/**
	 * 记录每个人携带的聚集点的编号消息
	 */
	public static final String SHOP = "shop";
	public PrintWriter pw_shop;
	// 用来记录每一步下每个人的空间位置坐标
	public PrintWriter pw_positionRecords;
	/**
	 * 记录每个STEP里聚合点情况。
	 */
	public static final String AGGRE = "aggre";
	/**
	 * 分数。
	 */
	public static final String SCORE = "score.txt";
	public PrintWriter pw_aggre;
	// 以下是用于实现多次测试的变量
	/**
	 * 试验次数
	 */
	public static int Times = 200;
	/**
	 * 两次试验间隔
	 */
	public static int Csapce = 1000;
	/**
	 * 计算当前次数
	 */
	public int ctimes = 1;
	/**
	 * 计算当前的步数
	 */
	public int cstep = 0;
	/**
	 * 表示实验开始
	 */
	public boolean isBegin = false;
	/**
	 * 表示存储文件夹
	 */
	public static String FloderName = "time";

	public int pgNum = 2;
	public int f = 80;
	public float temp = 4f;// 存储人与人之间消息传递的最小值

	public boolean RESET = false;

	// 在此变量结束

	@Override
	public void initTest(boolean deserialized) {
		if (deserialized)
			return;
		if (pw_path != null)
			pw_path.close();
		if (pw_shop != null)
			pw_shop.close();
		if (pw_aggre != null)
			pw_aggre.close();
		if (pw_positionRecords != null)
			pw_positionRecords.close();
		configure = FileIO.readConfigure();
		getWorld().setGravity(new Vec2());
		mall = Mall.initMall(getWorld());
		pgList.clear();
		pgList.addAll(mall.createPeopleGroup(pgNum));
		aggre.clear();
		people.clear();
		for (int i = 0; i < pgList.size(); i++) {
			PeopleGroup pg = pgList.get(i);
			people.add(pg.master);
			people.addAll(pg.others);

			// 初始化时每个人产生一个动作
			for (Body body : people) {
				if (((People) body.getUserData()).actionList.size() == 0) {
					((People) body.getUserData()).generateRandomAction();
				}
			}

		}

	}

	@Override
	public void mouseDown(Vec2 p, int button) {
		super.mouseDown(p, button);
	}

	/**
	 * 按s键，模拟实验开始,e结束(记录得分)。
	 */
	@Override
	public void keyPressed(char keyChar, int keyCode) {
		super.keyPressed(keyChar, keyCode);
		if (KeyEvent.VK_S == keyCode) {
			isBegin = true;
			try {
				// pw_path = new PrintWriter(new FileWriter(PATH,true));
				pw_aggre = new PrintWriter(AGGRE + "_" + pgNum + "_" + Aggregation.Default_T + "_"
						+ Aggregation.attract_radius + "_" + ".txt");
				pw_shop = new PrintWriter(SHOP + "_" + pgNum + "_" + Aggregation.Default_T + "_"
						+ Aggregation.attract_radius + "_" + ".txt");
				// pw_positionRecords = new PrintWriter("positionRecords" + "_"
				// + configure.getProperty("pgNum") + "_"
				// + configure.getProperty("T" + 1) + "_"
				// + configure.getProperty("attract_radius" + 1) + ".txt");
			} catch (IOException e) {
				e.printStackTrace();
			}
		} else if (KeyEvent.VK_E == keyCode) {
			if (pw_path != null) {
				pw_path.close();
			}
			pw_aggre.close();
			pw_shop.close();
			// pw_positionRecords.close();

			PrintWriter pw_score = null;
			try {
				pw_score = new PrintWriter(SCORE);
				for (int i = 0; i < pgList.size(); i++) {
					PeopleGroup pg = pgList.get(i);
					pw_score.println(pg.id);
					for (Body b : pg.score.keySet()) {
						pw_score.println(((People) (b.getUserData())).id + " " + pg.score.get(b));
					}
					pw_score.println();
					pg.initScore();
				}
				pw_score.flush();
			} catch (FileNotFoundException e) {
				e.printStackTrace();
			} finally {
				if (pw_score != null) {
					pw_score.close();
				}
			}
		}
	}

	@Override
	public void step(TestbedSettings settings) {
		super.step(settings);
		{
			addTextLine("step:" + getStepCount());
			addTextLine("cstep:" + cstep);
		}
		printOneStep();
		if (isBegin) {
			if (ctimes <= Times && cstep == 0) {
				if (RESET) {
					// if (Aggregation.attract_radius == 10
					// || Aggregation.attract_radius == 17) {
					// Aggregation.attract_radius += 3;
					// } else {
					// Aggregation.attract_radius += 2;
					// }
					// pgNum += 25;
					// f += 10;
					Aggregation.Default_T += 10;
					if (Aggregation.Default_T == 120) {
						pw_path.close();
						pw_aggre.close();
						pw_shop.close();
					}
					for (int i = 0; i < people.size(); i++) {
						getWorld().destroyBody(people.get(i));
					}
					for (int i = 0; i < aggre.size(); i++) {
						getWorld().destroyBody(aggre.get(i));
					}
					if (pw_path != null)
						pw_path.close();
					if (pw_shop != null)
						pw_shop.close();
					if (pw_aggre != null)
						pw_aggre.close();
					mall = Mall.initMall(getWorld());
					pgList.clear();
					pgList.addAll(mall.createPeopleGroup(pgNum));
					aggre.clear();
					people.clear();
					for (int i = 0; i < pgList.size(); i++) {
						PeopleGroup pg = pgList.get(i);
						people.add(pg.master);
						people.addAll(pg.others);

						// 每次实验每个人产生一个动作
						for (Body body : people) {
							if (((People) body.getUserData()).actionList.size() == 0) {
								((People) body.getUserData()).generateRandomAction();
							}
						}

					}
					System.out.println(Aggregation.Default_T);
				}
				try {
					// 同步模拟实验数据记录
					pw_aggre = new PrintWriter(FloderName + "/" + AGGRE + "_" + pgNum + "_" + Aggregation.Default_T
							+ "_" + Aggregation.attract_radius + "_" + ctimes + ".txt");
					// 异步模拟实验数据记录
					pw_shop = new PrintWriter(FloderName + "/" + SHOP + "_" + pgNum + "_" + Aggregation.Default_T + "_"
							+ Aggregation.attract_radius + "_" + ctimes + ".txt");
					// 输出当前实验次数
					System.out.println("ctimes:" + ctimes);
				} catch (FileNotFoundException e) {
					e.printStackTrace();
				}
				RESET = false;
			}

			// 每一步每人产生一个新动作
			for (Body body : people) {
				((People) body.getUserData()).generateRandomAction();
			}

			if (ctimes > Times) {
				isBegin = false;
			}
			// 每一步遍历所有商店，每个商店有0.307%的概率成为新的宣传点,若重复，则不生成。
			int n = mall.shopList.size();
			for (int i = 0; i < n; i++) {
				if (mall.UsedAsPromotion[i] == false && Tool.probility(0.00307)) {
					mall.UsedAsPromotion[i] = true;
					Body b = mall.shopList.get(i).aggre.createAggregationBody(getWorld());
					aggre.add(b);
				}
			}

			cstep++;
			if (cstep > Csapce) {
				System.out.println("c>1000");
				cstep = 0;
				RESET = true;
				try {
					for (Body body : people) {
						((People) body.getUserData()).outActionlist(ctimes);
					}
					ActionsOutputer.customize();
				} catch (Exception e) {
					e.printStackTrace();
				}
				ctimes++;
			}
		}
		// pg 是否被吸引及被吸引后的行为
		// for (int j = 0; j < aggre.size(); j++) {
		// for (int i = 0; i < pgList.size(); i++) {
		// PeopleGroup pg = pgList.get(i);
		// Body b = pg.master;// master是否被吸引
		// People masterData = (People) b.getUserData();
		// Body aggreBody = aggre.get(j);
		// Vec2 aggreBodyPosition = aggreBody.getPosition();
		// Vec2 v = new Vec2(aggreBodyPosition.x - b.getPosition().x,
		// aggreBodyPosition.y - b.getPosition().y);
		// if (v.length() > ((Aggregation) aggreBody.getUserData()).attract_radius)
		// continue;// 人物未进入宣传点的吸引范围
		// if (!Tool.probility(((Aggregation)
		// aggreBody.getUserData()).attract_possible))
		// continue;// 人物进入了宣传点的吸引范围但是未被吸引
		// // 如果在该宣传点之前未被别的商店吸引
		// if (!masterData.isAttract) {
		// b.setLinearVelocity(v.mul(((People) (b.getUserData())).attract_speed /
		// v.length()));
		// masterData.isAttract = true;
		// // 将该人物距离目的地的距离记录下来
		// masterData.setaDistanceOfAttract(v.length());
		// masterData.destination = aggreBodyPosition.clone();
		// // for (int index = 0; index < mall.shopList.size();
		// // index++) {
		// // if (mall.shopList.get(index).aggre.equals(a)
		// // && pg.PatLastShop != index + 1) {
		// // pg.PatShop = index + 1;
		// // }
		// // }
		// }
		// // 如果在该宣传点之前已经被别的商店吸引
		// else if (masterData.isAttract) {
		// // 当人物当前位置到新的吸引人物的宣传点的距离大于到老的吸引人物的宣传点距离时则改变人物的目的地
		// if (v.length() < masterData.getaDistanceOfAttract()) {
		// b.setLinearVelocity(v.mul(((People) (b.getUserData())).attract_speed /
		// v.length()));
		// masterData.destination = aggreBodyPosition.clone();
		// }
		// }
		// // 不可能出现这种情况
		// else {
		// b.setLinearVelocity(People.randomNormalSpeed());
		// }
		//
		// for (int k = 0; k < pg.others.size(); k++) {
		// Body otherBody = pg.others.get(k); // 组内其他人是否被吸引
		// People otherData = (People) otherBody.getUserData();
		// v = new Vec2(aggreBodyPosition.x - otherBody.getPosition().x,
		// aggreBodyPosition.y - otherBody.getPosition().y);
		// if (v.length() > ((Aggregation) aggreBody.getUserData()).attract_radius)
		// continue;
		// if (!Tool.probility(((Aggregation)
		// aggreBody.getUserData()).attract_possible))
		// continue;
		// if (!otherData.isAttract) {
		// otherBody.setLinearVelocity(
		// v.mul(((People) (otherBody.getUserData())).attract_speed / v.length()));
		// otherData.isAttract = true;
		// // 将该人物距离目的地的距离记录下来
		// otherData.setaDistanceOfAttract(v.length());
		// otherData.destination = aggreBodyPosition.clone();
		// otherData.isAttract = true;
		// } else if (otherData.isAttract) {
		// // 当人物当前位置到新的吸引人物的宣传点的距离大于到老的吸引人物的宣传点距离时则改变人物的目的地
		// if (v.length() < otherData.getaDistanceOfAttract()) {
		// otherBody.setLinearVelocity(
		// v.mul(((People) (otherBody.getUserData())).attract_speed / v.length()));
		// otherData.destination = aggreBodyPosition.clone();
		// }
		// }
		// // 不可能出现这种情况
		// else {
		// otherBody.setLinearVelocity(People.randomNormalSpeed());
		// }
		// }
		// }
		// }
		for (int i = 0; i < pgList.size(); i++) {
			PeopleGroup pg = pgList.get(i);
			Body b = pg.master;// master是否被吸引
			People px = (People) b.getUserData();
			for (int j = 0; j < aggre.size(); j++) {
				Body a = aggre.get(j);
				Vec2 p = a.getPosition();
				Vec2 v = new Vec2(p.x - b.getPosition().x, p.y - b.getPosition().y);
				if (v.length() > ((Aggregation) a.getUserData()).attract_radius)
					continue;// 未到达聚集点
				if (!Tool.probility(((Aggregation) a.getUserData()).attract_possible))
					continue;// 未被吸引
				if (!px.isAttract) {
					b.setLinearVelocity(v.mul(((People) (b.getUserData())).attract_speed / v.length()));
					px.isAttract = true;
					px.destination = p.clone();
					// for (int index = 0; index < mall.shopList.size(); index++) {
					// if (mall.shopList.get(index).aggre.equals(a)
					// && pg.PatLastShop != index + 1) {
					// pg.PatShop = index + 1;
					// }
					// }
				} else if (px.isAttract) {
					b.setLinearVelocity(v.mul(((People) (b.getUserData())).attract_speed / v.length()));
					px.destination = p.clone();
				} else {
					b.setLinearVelocity(People.randomNormalSpeed());
				}
			}
			for (int j = 0; j < pg.others.size(); j++) {
				Body o = pg.others.get(j); // 组内其他人是否被吸引
				People other = (People) o.getUserData();
				for (int k = 0; k < aggre.size(); k++) {
					Body ag = aggre.get(k);
					Vec2 p = ag.getPosition();
					Vec2 v = new Vec2(p.x - o.getPosition().x, p.y - o.getPosition().y);
					if (v.length() > ((Aggregation) ag.getUserData()).attract_radius)
						continue;
					if (!Tool.probility(((Aggregation) ag.getUserData()).attract_possible))
						continue;
					if (!other.isAttract) {
						o.setLinearVelocity(v.mul(((People) (o.getUserData())).attract_speed / v.length()));
						other.isAttract = true;
						other.destination = p.clone();
						other.isAttract = true;
					} else if (other.isAttract) {
						o.setLinearVelocity(v.mul(((People) (o.getUserData())).attract_speed / v.length()));
						other.destination = p.clone();
					} else {
						o.setLinearVelocity(People.randomNormalSpeed());
					}
				}
			}
		}
		this.TestAgg();
	}

	@Override
	public String getTestName() {
		return "Simulation Test";
	}

	/**
	 * 当且仅当isBegin==true时，打印每一个step的情况。
	 */
	public void printOneStep() {
		if (cstep == 0)
			return;
		// 记录每步每人所属群组号和坐标
		// for (int i = 0; i < people.size(); i++) {
		// Body b = people.get(i);
		// pw_positionRecords.printf("%d %.2f %.2f ", b.pgNo,
		// b.getPosition().x, b.getPosition().y);
		// }
		// pw_positionRecords.println("\n");
		// pw_positionRecords.flush();
		for (int i = 0; i < mall.shopList.size(); i++) {
			Shop s = mall.shopList.get(i);
			// 同步模拟实验数据写入
			pw_aggre.print(
					(mall.UsedAsPromotion[i] ? 1 : 0) + "," + s.id + "," + s.aggre.densityOfPeople(pgList) + " ");
			if (s.aggre.densityOfPeople(pgList) >= s.aggre.AGGRE_CRITICAL_VALUE && mall.UsedAsPromotion[i]) {
				mall.UsedAsAggregation[i] = true;
				s.aggre.PgatShop(pgList);
				for (int j = 0; j < people.size(); j++) {
					Body b1 = people.get(j);
					People p1 = (People) b1.getUserData();
					for (int k = 0; k < people.size(); k++) {
						Body b = people.get(k);
						People p = (People) b.getUserData();
						float distant = MathUtils.distance(b.getPosition(), b1.getPosition());
						// 人与人之间可以传递消息,共4种模式
						if (distant <= 4f && p1.pAtshop == -1 && p.pAtshop != -1 && p.isAttract && distant < temp) {
							temp = distant;
							if (b.isMaster && (!b1.isMaster) && b.pgNo == b1.pgNo && Tool.probility(0.9)) {
								p1.isAttract = true;
								p1.pAtshop = p.pAtshop;
								for (int m = 0; m < aggre.size(); m++) {
									Body ag = aggre.get(m);
									Vec2 p2 = ag.getPosition();
									if (p.destination != null && p.destination.equals(p2)) {
										p1.destination = p2.clone();
										p1.visitShop.add((Aggregation) ag.getUserData());
									}
								}
							} else if (b.isMaster && b1.isMaster && b.pgNo != b1.pgNo && Tool.probility(0.8)) {
								p1.isAttract = true;
								p1.pAtshop = p.pAtshop;
								for (int m = 0; m < aggre.size(); m++) {
									Body ag = aggre.get(m);
									Vec2 p2 = ag.getPosition();
									if (p.destination != null && p.destination.equals(p2)) {
										p1.destination = p2.clone();
										p1.visitShop.add((Aggregation) ag.getUserData());
									}
								}
							} else if (!b.isMaster && b.pgNo == b1.pgNo && b1.isMaster && Tool.probility(0.7)) {
								p1.isAttract = true;
								p1.pAtshop = p.pAtshop;
								for (int m = 0; m < aggre.size(); m++) {
									Body ag = aggre.get(m);
									Vec2 p2 = ag.getPosition();
									if (p.destination != null && p.destination.equals(p2)) {
										p1.destination = p2.clone();
										p1.visitShop.add((Aggregation) ag.getUserData());
									}
								}
							} else if (!b.isMaster && b.pgNo != b1.pgNo && !b1.isMaster && Tool.probility(0.6)) {
								p1.isAttract = true;
								p1.pAtshop = p.pAtshop;
								for (int m = 0; m < aggre.size(); m++) {
									Body ag = aggre.get(m);
									Vec2 p2 = ag.getPosition();
									if (p.destination != null && p.destination.equals(p2)) {
										p1.destination = p2.clone();
										p1.visitShop.add((Aggregation) ag.getUserData());
									}
								}
							}
						}
						// 如果本组中除了master以外的百分之80以上的人都成功被同一个聚集点吸引，那么整组就被该聚集点吸引
						// 如果本组中除了百分之80以上的人或者master想要离开当前聚集点，那么整组就会离开该聚集点
						// int count1 = 0;
						// int count2 = 0;
						// if (p.isAttract && p1.isAttract
						// && p.pAtshop == p1.pAtshop && p.pAtshop != -1
						// && p1.pAtshop != -1
						// && isInTheSameGroup(b1, b, pg2)) {
						// count1++;
						// }
						// if (Tool.probility(0.2) && Tool.probility(0.2) &&
						// !isLeave) {
						// p.leaveAggre = true;
						// p1.leaveAggre = true;
						// if (p.isAttract && p1.isAttract
						// && p.pAtshop == p1.pAtshop
						// && isInTheSameGroup(b1, b, pg2)) {
						// count2++;
						// }
						// }

						// if (count1 / (pg2.others.size() + 1) >= 0.8) {
						// People master = (People) pg2.master.getUserData();
						// for (int a = 0; a < aggre.size(); a++) {
						// Body ag = aggre.get(a);
						// Vec2 p3 = ag.getPosition();
						// if (p.destination != null
						// && p.destination.equals(p3)) {
						// master.destination = p3.clone();
						// master.pAtshop = p.pAtshop;
						// master.isAttract = true;
						// }
						// }
						// }
						// if ((count2 + 1) / (pg2.others.size() + 1) >= 0.8) {
						// isLeave = true;
						// People master = (People) pg2.master.getUserData();
						// pg2.PatLastShop = master.pAtshop;
						// pg2.PatShop = -1;
						// master.pAtshop = -1;
						// master.destination = null;
						// master.isAttract = false;
						// for (int m = 0; m < pg2.others.size(); m++) {
						// Body b4 = pg2.others.get(m);
						// People p4 = (People) b4.getUserData();
						// p4.pAtshop = -1;
						// p4.destination = null;
						// p4.isAttract = false;
						// }
						// }
						// if (isLeave) {
						// for (Body b2 : pg2.others) {
						// People p2 = (People) b2.getUserData();
						// p2.leaveAggre = false;
						// }
						// }
					}
					pw_shop.print(p1.id + "," + p1.pAtshop + "," + p1.lastShop + " ");
				}
				pw_shop.println();
			} else if (mall.UsedAsAggregation[i] && s.aggre.densityOfPeople(pgList) < s.aggre.AGGRE_CRITICAL_VALUE) {
				mall.UsedAsAggregation[i] = false;
				s.aggre.PgNotAtShop(pgList);
			}
		}
		pw_aggre.println();
		pw_aggre.flush();
		pw_shop.flush();
	}

	/**
	 * 判断当前2人是否在同一组
	 */
	public boolean isInTheSameGroup(Body p1, Body p2, PeopleGroup pg) {

		if (pg.others.contains(p1) && pg.others.contains(p2)) {
			return true;
		} else if (pg.master.equals(p1) && pg.others.contains(p2)) {
			return true;
		} else if (pg.others.contains(p1) && pg.master.equals(p2)) {
			return true;
		} else {
			return false;
		}
	}

	/**
	 * 测试当前的宣传点是否有到期的,到期就删除,同时所有目的地为此删除的Aggregation的人的目的地置为空,isAtract为false。
	 */
	public void TestAgg() {
		List<Body> remove = new ArrayList<Body>();
		for (Body b : this.aggre) {
			Aggregation a = (Aggregation) b.getUserData();
			if (a.t != 0) {
				a.t--;
			} else {
				getWorld().destroyBody(b);
				a.t = a.T;
				for (int i = 0; i < mall.shopList.size(); i++) {
					Shop s = mall.shopList.get(i);
					if (a.equals(s.aggre)) {
						mall.UsedAsPromotion[i] = false;
						mall.UsedAsAggregation[i] = false;
						break;
					}
				}
				remove.add(b);
			}
		}
		aggre.removeAll(remove);
		for (int i = 0; i < pgList.size(); i++) {
			PeopleGroup pg = pgList.get(i);
			Body b = pg.master;
			People px = (People) b.getUserData();
			for (int j = 0; j < remove.size(); j++) {
				Aggregation a = (Aggregation) remove.get(j).getUserData();
				if (px.visitShop.contains(a) || px.pAtshop == a.id) {
					px.lastShop = a.id;
					px.visitShop.remove(a);
				}
				px.destination = null;
				px.isAttract = false;
				for (int k = 0; k < pg.others.size(); k++) {
					Body o = pg.others.get(k);
					People po = (People) o.getUserData();
					if (po.pAtshop == a.id || po.visitShop.contains(a)) {
						// po.start = 0;
						po.lastShop = a.id;
						po.visitShop.remove(a);
					}
					po.destination = null;
					po.isAttract = false;
				}
			}
			pg.maintain();
		}
	}

}
