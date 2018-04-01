package model;

import java.util.ArrayList;
import java.util.List;
import java.util.Random;

import org.jbox2d.collision.shapes.CircleShape;
import org.jbox2d.common.MathUtils;
import org.jbox2d.common.Vec2;
import org.jbox2d.dynamics.Body;
import org.jbox2d.dynamics.BodyDef;
import org.jbox2d.dynamics.BodyType;
import org.jbox2d.dynamics.World;

import test.ActionsOutputer;

public class People {
	public static final float PEOPLE_RADIUS = 0.3f;
	public int id;
	// 记录所携带的聚集点信息
	public int pAtshop;
	public List<Aggregation> visitShop;
	
	private int pre_action = -1;
	private int count = 0;
	private int size = 4;
	
	public List<Integer> actionList;    //动作列表

	/**
	 * 判断当前是否有被吸引
	 */
	public boolean isAttract = false;
	/**
	 * 目的地。
	 */
	public Vec2 destination;
	/**
	 * 正常时候的速度。
	 */
	public float walk_speed = 1.4f;
	/**
	 * 被吸引的速度
	 */
	public float attract_speed = 4.0f * 10;
	/**
	 * 当前运行速度的方向
	 */
	public Vec2 speed;
	/**
	 * 存储与该人正在交流的人的信息
	 */
	public List<People> chatMember;
	/**
	 * 人是否想要离开当前聚集点
	 */
	public boolean leaveAggre = false;
	/**
	 * 人所在的上次已经广播结束消息的商店
	 */
	public int lastShop;

	public People() {
		this.pAtshop = -1;
		this.lastShop = -1;
		this.actionList = new ArrayList<Integer>();
	}

	public People(int id) {
		this.id = id;
		this.pAtshop = -1;
		this.lastShop = -1;
		this.visitShop = new ArrayList<Aggregation>();
		this.actionList = new ArrayList<Integer>();
	}

	enum PeopleType {
		Kid, MAN, WOMEN, OLD
	}

	

	
	/**
	 * 随机向w世界加入一个id标识的人。
	 * 
	 * @param w
	 * @param id
	 * @return
	 */
	public static Body createPeopleBody(World w, int id) {
		BodyDef peopleDef = new BodyDef();
		peopleDef.linearDamping = 0.0f;
		peopleDef.angularDamping = 1.0f;
		peopleDef.type = BodyType.DYNAMIC;
		peopleDef.linearVelocity = randomNormalSpeed();
		float x = MathUtils.randomFloat(-50, 50);
		float y = MathUtils.randomFloat(0, 100);
		peopleDef.position = new Vec2(x, y);
		Body p = w.createBody(peopleDef);
		CircleShape peopleShape = new CircleShape();
		peopleShape.setRadius(People.PEOPLE_RADIUS);

		p.createFixture(peopleShape, 3.0f);
		p.setUserData(new People(id));
		
		return p;
	}

	/**
	 * 随机向w世界加入一个id标识的人,此人离vec2的最大距离不超过maxDistance。
	 * 
	 * @param w
	 * @param id
	 * @return
	 */
	public static Body createPeopleBody(World w, int id, Vec2 vec2,
			float maxDistance) {
		BodyDef peopleDef = new BodyDef();
		peopleDef.linearDamping = 0.0f;
		peopleDef.angularDamping = 1.0f;
		peopleDef.type = BodyType.DYNAMIC;
		peopleDef.linearVelocity = randomNormalSpeed();
		float x;
		float y;
		do {
			x = MathUtils.randomFloat(vec2.x - maxDistance, vec2.x
					+ maxDistance);
			y = MathUtils.randomFloat(vec2.y - maxDistance, vec2.y
					+ maxDistance);
			peopleDef.position = new Vec2(x, y);
		} while (x <= -50 || x > 50 || y <= 0 || y >= 100
				|| MathUtils.distance(vec2, peopleDef.position) >= maxDistance);

		Body p = w.createBody(peopleDef);
		CircleShape peopleShape = new CircleShape();
		peopleShape.setRadius(People.PEOPLE_RADIUS);

		p.createFixture(peopleShape, 3.0f);
		p.setUserData(new People(id));
		return p;
	}

	/**
	 * 人的正常随机速度。
	 * 
	 * @return
	 */
	public static Vec2 randomNormalSpeed() {
		Vec2 v = new Vec2(MathUtils.randomFloat(-2.0f, 2.0f),
				MathUtils.randomFloat(-2.0f, 2.0f));
		return v.mul(50);
	}

	/**
	 * 获取当前的速度
	 * 
	 * @param position
	 *            当前位置
	 * @return
	 */
	public Vec2 getSpeed(Vec2 position) {
		if (this.destination == null) {
			return null;
		} else {
			Vec2 x = this.destination.sub(position);
			x.normalize();
			return x.mulLocal(attract_speed);
		}
	}
	private float aDistanceOfAttract;
	public float getaDistanceOfAttract() {
		return aDistanceOfAttract;
	}

	public void setaDistanceOfAttract(float aDistanceOfAttract) {
		this.aDistanceOfAttract = aDistanceOfAttract;
	}

	/**
	 * 随机产生一个动作
	 * */
	public void generateRandomAction() {
		if(count > 0 && count < size) {
			actionList.add(pre_action);
			++count;
		}else if(count == size || count == 0) {
			Random random = new Random();
			int action;
			do {
				action = random.nextInt(10);
			}while(pre_action == action);
			pre_action = action;
			actionList.add(action);
			count = 1;
		}
		
	}
	
	/**
	 * 输出动作序列
	 */
	
	public void outActionlist(int ctimes) throws Exception{
		ActionsOutputer.writeCSV(actionList, ctimes, id);
	}
	
//	/**
//	 * 整合动作数据（由于会大大拖慢模拟器进程，不再启用）
//	 * */
//	public void actionDataCompound(int ctimes) throws Exception{
//		for(int i=0;i<actionList.size();i++) {
//			ActionDataCompound.DataCompound(actionList.get(i), id, ctimes);
//		}
//		
//	}

}
