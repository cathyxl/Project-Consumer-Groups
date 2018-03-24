package model;

import java.util.ArrayList;
import java.util.List;

import org.jbox2d.collision.shapes.CircleShape;
import org.jbox2d.common.MathUtils;
import org.jbox2d.common.Vec2;
import org.jbox2d.dynamics.Body;
import org.jbox2d.dynamics.BodyDef;
import org.jbox2d.dynamics.BodyType;
import org.jbox2d.dynamics.World;

public class Aggregation {
	/**
	 * 判断是否聚集的临界值
	 */
	public static final float AGGRE_CRITICAL_VALUE = (float) (50 / (Math.PI * 8f * 8f));
	/**
	 * 给出两次聚集的统计间隔时间
	 */
	public static int STEP = 500;
	/**
	 * 给出聚集点的宣传时间
	 */
	public static int Default_T = 50;

	/**
	 * 将某些修改变量重置为初始
	 */
	// public static void reback() {
	// STEP = 60;
	// Default_T = 80;
	//
	// }

	/**
	 * 与shop对应。
	 */
	public int id;
	/**
	 * 宣传点的吸引半径
	 */
	public static int attract_radius = 15;
	/**
	 * 宣传点的吸引概率
	 */
	public double attract_possible = 0.49;
	/**
	 * 判定成功进入宣传点的半径
	 */
	public float attract_in = 8f;
	/**
	 * 宣传剩余时间。
	 */
	public static int t = Default_T * 10;
	/**
	 * 宣传总时间。
	 */
	public static int T = Default_T * 10;

	/**
	 * 宣传的中心点
	 */
	public Vec2 center;
	/**
	 * 宣传点内的人
	 */
	public List<People> pg;

	public Aggregation(int id, int attract_radius, double d, int T, Vec2 center) {
		super();
		this.id = id;
		this.attract_radius = attract_radius;
		this.attract_possible = d;
		this.T = T;
		this.t = T;
		this.center = center;
		this.pg = new ArrayList<People>();
	}

	/**
	 * 在世界w里构造AggregationBody，把当前Aggregation信息存入body中。
	 * 
	 * @param w
	 * @return
	 */
	public Body createAggregationBody(World w) {
		BodyDef bd = new BodyDef();
		bd.position = center;
		CircleShape cs = new CircleShape();
		cs.setRadius(1);
		Body b = w.createBody(bd);
		b.createFixture(cs, 0);
		b.setUserData(this);
		return b;
	}

	/**
	 * 宣传点周围半径r范围内人的密度（人的数量除以面积）。
	 * 
	 * @param People
	 * @return
	 */
	public float densityOfPeople(List<PeopleGroup> pgList) {
		int count = 0;
		for (int i = 0; i < pgList.size(); i++) {
			PeopleGroup pg = pgList.get(i);
			Body b = pg.master;
			if (MathUtils.distance(center, b.getPosition()) < attract_in) {
				count++;
			}
			for (int j = 0; j < pg.others.size(); j++) {
				Body o = pg.others.get(j);
				if (MathUtils.distance(center, o.getPosition()) < attract_in) {
					count++;
				}
			}
		}
		float density = count / (MathUtils.PI * attract_in * attract_in);
		return density;
	}

	/**
	 * 在聚集点周围半径r内的人将获得聚集点信息
	 */
	public void PgatShop(List<PeopleGroup> pgList) {
		for (int i = 0; i < pgList.size(); i++) {
			PeopleGroup pg = pgList.get(i);
			Body b = pg.master;
			People p = (People) b.getUserData();
			if (MathUtils.distance(center, b.getPosition()) < attract_in) {
				p.pAtshop = id;
//				pg.PatShop = id;
				p.visitShop.add(this);
			}
			for (int j = 0; j < pg.others.size(); j++) {
				Body o = pg.others.get(j);
				People po = (People) o.getUserData();
				if (MathUtils.distance(center, o.getPosition()) < attract_in) {
					po.pAtshop = id;
					po.visitShop.add(this);
				}
			}

		}

	}

	/**
	 * 当聚集点的人群密度降低到一定值的时候,将人携带的商店信息重置
	 */
	public void PgNotAtShop(List<PeopleGroup> pgList) {
		for (int i = 0; i < pgList.size(); i++) {
			PeopleGroup pg = pgList.get(i);
			Body b = pg.master;
			People p = (People) b.getUserData();
			if (p.pAtshop == id || p.visitShop.contains(this)) {
				p.lastShop = id;
				p.visitShop.remove(this);
				// p.start = 0;
			}
			for (int j = 0; j < pg.others.size(); j++) {
				Body o = pg.others.get(j);
				People po = (People) o.getUserData();
				if (po.pAtshop == id || p.visitShop.contains(this)) {
					// po.start = 0;
					po.lastShop = id;
					po.visitShop.remove(this);
				}
			}

		}

	}
}
