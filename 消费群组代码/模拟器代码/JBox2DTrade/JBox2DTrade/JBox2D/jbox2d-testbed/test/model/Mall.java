package model;

import java.util.ArrayList;
import java.util.List;

import org.jbox2d.collision.shapes.EdgeShape;
import org.jbox2d.common.MathUtils;
import org.jbox2d.common.Vec2;
import org.jbox2d.dynamics.Body;
import org.jbox2d.dynamics.BodyDef;
import org.jbox2d.dynamics.BodyType;
import org.jbox2d.dynamics.World;
import org.jbox2d.testbed.framework.TestbedSettings;

public class Mall {
	/**
	 * 地图比例尺
	 */
	public static final float m = 0.125f;

	private final World w;

	private final Body ground;

	public List<Shop> shopList = new ArrayList<Shop>();
	/**
	 * 与shopList对应，当一个商店选为Aggregation，则对应位置置为true。
	 */
	public boolean[] UsedAsPromotion;
	public boolean[] UsedAsAggregation;
	public TestbedSettings settings;

	public Mall(World w){
		this.w = w;
		BodyDef bd = new BodyDef();
		ground = w.createBody(bd);
	}

	enum ShopType {
		RIGHT, LEFT, UP, DOWN
	}

	public class Shop {
		public int id;
		public Vec2 position;
		public Aggregation aggre;

		/**
		 * 生成一个Shop对象
		 * 
		 * @param v1
		 * @param v2
		 * @param st
		 */
		public Shop(int count, Vec2 v1, Vec2 v2, ShopType st) {
			this.id = count;
			BodyDef pillarDef = new BodyDef();
			pillarDef.position.set(new Vec2((v1.x + v2.x) / 2,
					(v1.y + v2.y) / 2));
			position = pillarDef.position.clone();
			float hx = MathUtils.abs(v1.x - v2.x) / 2;
			float hy = MathUtils.abs((v1.y - v2.y)) / 2;
			List<Vec2> a = new ArrayList<Vec2>();
			if (st == ShopType.DOWN) {
				a.add(new Vec2(position.x - hx, position.y - hy));
				a.add(new Vec2(position.x - hx, position.y + hy));
				a.add(new Vec2(position.x + hx, position.y + hy));
				a.add(new Vec2(position.x + hx, position.y - hy));
				this.aggre = new Aggregation(id, Aggregation.attract_radius,
						0.49, Aggregation.T, new Vec2(position.x, position.y
								- hy));
			} else if (st == ShopType.LEFT) {
				a.add(new Vec2(position.x - hx, position.y + hy));
				a.add(new Vec2(position.x + hx, position.y + hy));
				a.add(new Vec2(position.x + hx, position.y - hy));
				a.add(new Vec2(position.x - hx, position.y - hy));
				this.aggre = new Aggregation(id, Aggregation.attract_radius,
						0.49, Aggregation.T, new Vec2(position.x - hx,
								position.y));
			} else if (st == ShopType.UP) {
				a.add(new Vec2(position.x + hx, position.y + hy));
				a.add(new Vec2(position.x + hx, position.y - hy));
				a.add(new Vec2(position.x - hx, position.y - hy));
				a.add(new Vec2(position.x - hx, position.y + hy));
				this.aggre = new Aggregation(id, Aggregation.attract_radius,
						0.49, Aggregation.T, new Vec2(position.x, position.y
								+ hy));
			} else {
				a.add(new Vec2(position.x + hx, position.y - hy));
				a.add(new Vec2(position.x - hx, position.y - hy));
				a.add(new Vec2(position.x - hx, position.y + hy));
				a.add(new Vec2(position.x + hx, position.y + hy));
				this.aggre = new Aggregation(id, Aggregation.attract_radius,
						0.49, Aggregation.T, new Vec2(position.x + hx,
								position.y));
			}
			drawPolygon(a);
		}
	}


	public static Mall initMall(World w) {
		Mall mall = new Mall(w);
		int count = 0;
		for (int i = 0; i < 3; i++) {
			count++;
			mall.shopList.add(mall.new Shop(count, new Vec2(-50 + i * 30, 90),
					new Vec2(-20 + i * 30, 100), ShopType.DOWN));
		}
		for (int i = 0; i < 3; i++) {
			count++;
			mall.shopList.add(mall.new Shop(count, new Vec2(40, 100 - i * 30),
					new Vec2(50, 70 - i * 30), ShopType.LEFT));
		}
		for (int i = 0; i < 3; i++) {
			count++;
			mall.shopList.add(mall.new Shop(count, new Vec2(50 - i * 30, 10),
					new Vec2(20 - i * 30, 0), ShopType.UP));
		}
		for (int i = 0; i < 3; i++) {
			count++;
			mall.shopList.add(mall.new Shop(count, new Vec2(-50, i * 30),
					new Vec2(-40, 30 + i * 30), ShopType.RIGHT));
		}
		mall.UsedAsPromotion = new boolean[mall.shopList.size()];
		mall.UsedAsAggregation = new boolean[mall.shopList.size()];
		return mall;
	}

	/**
	 * 
	 * @param count
	 *            人数
	 */
	public List<Body> createPeople(int count) {
		List<Body> list = new ArrayList<Body>();
		for (int i = 0; i < count; i++) {
			Body p = People.createPeopleBody(w, i);
			list.add(p);
		}
		return list;
	}

	/**
	 * 每组0到8人
	 * 
	 * @param groupCount
	 *            组数
	 */
	public List<PeopleGroup> createPeopleGroup(int groupCount) {
		List<PeopleGroup> list = new ArrayList<PeopleGroup>();
		int count = 0;
		for (int i = 0; i < groupCount; i++) {
			Body master = People.createPeopleBody(w, count);
			master.isMaster = true;
			count++;
//			int rand = (int) (Math.random() * 9);
			int rand = 4;// 每个人群的人数
			List<Body> others = new ArrayList<Body>();
			for (int j = 0; j < rand; j++) {
				Body other = People.createPeopleBody(w, count,
						master.getPosition(), PeopleGroup.RADIUS);
				other.isMaster = false;
				others.add(other);
				count++;
			}
			PeopleGroup pg = new PeopleGroup(i, master, others);
			list.add(pg);
		}
		return list;
	}

	private void drawPolygon(List<Vec2> veclist) {
		for (int i = 0; i < veclist.size(); i++) {
			if (i + 1 != veclist.size()) {
				drawLineOnGround(veclist.get(i), veclist.get(i + 1));
			}
		}
	}

	private void drawLineOnGround(Vec2 vec1, Vec2 vec2) {
		EdgeShape edge = new EdgeShape();
		edge.set(vec1, vec2);
		ground.createFixture(edge, 0);
	}

	/**
	 * 获取当前Mall的World对象
	 * 
	 * @return
	 */
	public World getWorld() {
		return w;
	}

	/**
	 * 以V为中心建立宣传点
	 * 
	 * @param v
	 */
	public void createAggre(Vec2 v) {

	}

}
